"""
Defines the datastore and all interfaces needed for a Observacion in the platform
"""
__author__ = 'Cesar'

import logging
from google.appengine.ext import ndb
from casilla import Casilla
from observador import Observador
from media import Media
from nota import Nota

class Observacion(ndb.Model):
    """
    Represents a observacion of a Casilla in the platform.

        - observador: Author of this Observacion
        - media: Any media related to the Observacion
        - nota: Any nota related to the Observacion
    """

    date = ndb.DateTimeProperty(auto_now_add=True)
    casilla = ndb.KeyProperty(kind=Casilla)
    observador = ndb.KeyProperty(kind=Observador)
    media = ndb.KeyProperty(kind=Media)
    nota = ndb.KeyProperty(kind=Nota)

    @classmethod
    def save_to_datastore(cls, observador, casilla, media, m_type, nota):
        """
        Saves a Observacion as a new entity on the datastore. Creates new media and nota entities if necessary
        Args:
            observador: (String) email
            casilla: (String) national id
            media: (String)
            nota: (String)

        Returns:
            True if creation successful, exception otherwise
        """
        try:
            c = Casilla.get_from_datastore(casilla)
            o = Observador.get_from_datastore(observador)
            m = Media.create(name=media, m_type=m_type)
            n = Nota.create(nota)
            new = Observacion(casilla=c.key,
                              observador=o.key,
                              media=m,
                              nota=n)
            key = new.put()
        except Exception as e:
            logging.exception("[Observacion] - "+e.message)
            raise ObservacionCreationError('Error creating the observacion in datastore: '+e.__str__())
        else:
            logging.debug('[Observacion] - New Observacion, Key = {0}'.format(key))
            return True


class ObservacionCreationError(Exception):
    def __init__(self, value):
        self.value = value
        logging.exception('[Observacion] - Observacion Error:'+value, exc_info=True)

    def __str__(self):
        return repr(self.value)
