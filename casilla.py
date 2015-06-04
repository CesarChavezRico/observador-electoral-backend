"""
Defines the datastore and all interfaces needed for a Casilla in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb
from google.appengine.api import search

from observador import Observador
from distrito import Distrito


class Casilla(ndb.Model):
    """
    Represents a casilla within the platform.

        - loc:          Lat, Lon
        - name:
        - address:
        - picture_url:
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    observador = ndb.KeyProperty(kind=Observador)
    distrito = ndb.KeyProperty(kind=Distrito)
    national_id = ndb.StringProperty()
    loc = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    picture_url = ndb.StringProperty()

    @classmethod
    def exists(cls, national_id):
        """
        Checks the datastore to find if the casilla (national_id) is already on it.

        Args:
            national_id: (String) national_id from request

        Returns:
            True if national_id exist False otherwise
        """
        return cls.query(cls.national_id == national_id).count(1) == 1

    @classmethod
    def create(cls, distrito, national_id, name, loc, address, picture_url):
        """
        Creates a new casilla in the datastore and a document for the Search API and includes it on the
        CasillasIndex.

        Args:
            - distrito:     String holding the name of the national id of the Distrito this Casilla belongs to
            - national_id   String holding the national_id for the casilla
            - name:         String holding the name of the casilla
            - loc:          String holding Lat, Lon of the casilla
            - address:      String holding the address of the location
            - picture_url:  String holding the url of the picture for the location

        Returns:
            Key of new entity
        """
        try:
            d = Distrito.get_from_datastore(distrito)
            distrito_key = d.key
            geo_pt = ndb.GeoPt(str(loc))
            o = Casilla(loc=geo_pt,
                        national_id=national_id,
                        distrito=distrito_key,
                        name=name,
                        address=address,
                        picture_url=picture_url)
            key = o.put()

            # Generate document for search API
            l_doc = search.Document(fields=[search.TextField(name='key',
                                                             value=str(key)),
                                            search.GeoField(name='loc',
                                                            value=search.GeoPoint(geo_pt.lat,
                                                                                  geo_pt.lon))])
            index = search.Index(name="CasillasIndex")
            index.put(l_doc)
        except Exception:
            logging.exception("[casilla] - Error in create Casilla", exc_info=True)
            raise CasillaCreationError('Error creating the casilla in platform')
        else:
            return key

    @classmethod
    def get_from_datastore(cls, national_id):
        """
        Gets a casilla from datastore based on its location
        """
        try:
            if Casilla.exists(national_id):
                query = Casilla.query(Casilla.national_id == national_id).fetch(limit=1)
                u = query
            else:
                raise GetCasillaError('Casilla does not exist')
        except Exception as e:
                raise GetCasillaError('Error getting Casilla: '+e.__str__())
        else:
            logging.debug("[Casilla] - Key = {0}".format(u[0].key))
            logging.debug("[Casilla] - location = {0}".format(u[0].loc))
            logging.debug("[Casilla] - national_id = {0}".format(u[0].national_id))
            logging.debug("[Casilla] - distrito = {0}".format(u[0].distrito))
            logging.debug("[Casilla] - name = {0}".format(u[0].name))
            logging.debug("[Casilla] - address = {0}".format(u[0].address))
            logging.debug("[Casilla] - picture_url = {0}".format(u[0].picture_url))
            return u[0]

    @classmethod
    def assign_to_observador(cls, email, account_number):
        """
        Assigns a Casilla to a observador (email) in the platform.

        Args:
            email: (String) email from Observador that will be assigned the Casilla
            national_id: (String) national_id of the casilla to assign

        Returns:
            True if assignment successful, False otherwise
        """
        try:
            o = Observador.get_from_datastore(email)
            c = Casilla.get_from_datastore(account_number)

            casilla = c.key.get()
            casilla.observador = o.key
            casilla.put()
        except GetCasillaError:
            raise
        except GetCasillaError:
            raise
        else:
            logging.debug("[Casilla] - assign_to_observador(): Assignment successful!"
                          " casilla = {0} assigned to observador = {1}"
                          .format(casilla.national_id, o.email))
            return True



class GetCasillaError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CasillaCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
