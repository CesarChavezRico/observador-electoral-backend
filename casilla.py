"""
Defines the datastore and all interfaces needed for a Casilla in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb
from google.appengine.api import search


class Casilla(ndb.Model):
    """
    Represents a casilla within the platform.

        - loc:          Lat, Lon
        - name:
        - address:
        - picture_url:
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    loc = ndb.GeoPtProperty()
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    picture_url = ndb.StringProperty()

    @classmethod
    def create(cls, name, loc, address, picture_url):
        """
        Creates a new casilla in the datastore and a document for the Search API and includes it on the
        CasillasIndex.

        Args:
            - name:         String holding the name of the location
            - loc:          String holding Lat, Lon of the location
            - address:      String holding the address of the location
            - picture_url:  String holding the url of the picture for the location

        Returns:
            Key of new entity
        """
        try:
            geo_pt = ndb.GeoPt(str(loc))
            o = Casilla(loc=geo_pt, name=name, address=address, picture_url=picture_url)
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
    def get_from_datastore(cls, email):
        """
        Gets a casilla from datastore based on its location
        """


class GetObservadorError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CasillaCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
