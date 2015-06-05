"""
Defines the datastore and all interfaces needed for a Observacion in the platform
"""
__author__ = 'Cesar'

import logging
from google.appengine.ext import ndb
from casilla import Casilla
from observador import Observador


class Observacion(ndb.Model):
    """
    Represents a observacion of a Casilla in the platform.

        - observador: Author of this Observacion
        - casilla: The casilla the Observacion is about
    """

    date = ndb.DateTimeProperty(auto_now_add=True)
    casilla = ndb.KeyProperty(kind=Casilla)
    observador = ndb.KeyProperty(kind=Observador)

    @classmethod
    def save_to_datastore(cls, observador, casilla):
        """
        Saves a Observacion as a new entity on the datastore.
        Args:
            observador: (String) email
            casilla: (String) national id


        Returns:
             If creation successful: URL safe key of the new observacion, exception otherwise
        """
        try:
            c = Casilla.get_from_datastore(casilla)
            o = Observador.get_from_datastore(observador)
            new = Observacion(casilla=c.key,
                              observador=o.key)
            key = new.put()
        except Exception as e:
            logging.exception("[Observacion] - "+e.message)
            raise ObservacionCreationError('Error creating the observacion in datastore: '+e.__str__())
        else:
            logging.debug('[Observacion] - New Observacion, Key = {0}'.format(key))
            return key.urlsafe()


class ObservacionCreationError(Exception):
    def __init__(self, value):
        self.value = value
        logging.exception('[Observacion] - Observacion Error:'+value, exc_info=True)

    def __str__(self):
        return repr(self.value)
