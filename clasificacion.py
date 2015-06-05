"""
Defines the datastore and all interfaces needed for a Clasificacion in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb



class Clasificacion(ndb.Model):
    """
    Represents a Clasificacion within the platform.

        - name:
        - checklist: JSON string of the checklist to fill for this Clasificacion
        - repeatable: Can only be performed once for a given Casilla
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    checklist = ndb.JsonProperty()
    repeatable = ndb.BooleanProperty()

    @classmethod
    def create(cls, name, checklist, repeatable):
        """
        Creates a new Clasificacion in the datastore.
        :param:
            - name: String holding the name of the Clasificacion
            - checklist: JSON string of the checklist to fill for this Clasificacion
            - repeatable: Can only be performed once for a given Casilla

        :return:
            Key of new entity
        """
        try:
            c = Clasificacion(name=name, checklist=checklist, repeatable=repeatable)
            key = c.put()

        except Exception:
            logging.exception("[Clasificacion] - Error in create Clasificacion", exc_info=True)
            raise ClasificacionCreationError('Error creating the Clasificacion in platform')
        else:
            return key

    @classmethod
    def get_available(cls, casilla):
        """
        Gets available clasificaciones for the requested casilla
        :param:
            - casilla: national_id (String) unique identifier of the Casilla in the national database

        :return:
            list of URL safe keys of clasificaciones
        """
        from observacion import Observacion

        try:
            # Get all clasificaciones
            query_response = Clasificacion.query()
            c_available = []
            for c in query_response:
                c_available.append(c.key.urlsafe())
            # Get observaciones for given casilla
            obs = Observacion.get_all(casilla)
            # Remove all clasificaciones already performed in an observacion if the clasificacion is not repeatable
            for i, o in enumerate(obs):
                clasificacion = o.clasificacion.get()
                logging.debug("[Clasificacion] - Clasificacion: {0}.repeatable = {1}"
                              .format(clasificacion.key, clasificacion.repeatable))
                if not clasificacion.repeatable:
                    c_available.pop(i)
            if c_available:
                pass
            else:
                raise GetClasificacionError('No available clasificaciones for Casilla: {0}'.format(casilla))
        except Exception:
            logging.exception("[Clasificacion] - Error in getting available Clasificaciones for Casilla: {0}"
                              .format(casilla), exc_info=True)
            raise GetClasificacionError('Error getting the Clasificacion')
        else:
            for c in c_available:
                logging.debug("[Clasificacion] = {0}".format(c))
            return c_available

    @classmethod
    def get_all(cls):
        """
        Gets all clasificaciones

        :return:
            list of URL safe keys of clasificaciones
        """

        try:
            # Get all clasificaciones
            query_response = Clasificacion.query()
            c_available = []
            for c in query_response:
                c_available.append(c.key.urlsafe())
            if c_available:
                pass
            else:
                raise GetClasificacionError('No available clasificaciones')
        except Exception:
            logging.exception("[Clasificacion] - Error in getting available Clasificaciones", exc_info=True)
            raise GetClasificacionError('Error creating the Clasificacion in platform')
        else:
            for c in c_available:
                logging.debug("[Clasificacion] = {0}".format(c))
            return c_available

    @classmethod
    def get_details(cls, url_safe_key):
        """
        Gets the details of a given (URL safe key) clasificacion

        :param url_safe_key

        :return:
            list of URL safe keys of clasificaciones
        """

        try:
            c = ndb.Key(urlsafe=url_safe_key)
            clasificacion = c.get()
            if not clasificacion:
                raise GetClasificacionError("[Clasificacion] - Error in getting {0} Clasificacion"
                                            .format(url_safe_key), exc_info=True)
        except Exception:
            logging.exception("[Clasificacion] - Error in getting {0} Clasificacion".format(url_safe_key),
                              exc_info=True)
            raise GetClasificacionError('Error creating the Clasificacion in platform')
        else:
            return clasificacion


class ClasificacionCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class GetClasificacionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



