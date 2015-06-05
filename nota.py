"""
Defines the datastore and all interfaces needed for a Nota in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb
from observacion import Observacion


class Nota(ndb.Model):
    """
    Represents a nota within the platform.

        - name: unique id for nota file in bucket
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    observacion = ndb.KeyProperty(kind=Observacion)
    name = ndb.StringProperty()

    @classmethod
    def exists(cls, name):
        """
        Checks the datastore to find if the nota (name) is already on it.

        Args:
            name: (String) type name request

        Returns:
            True if name exist False otherwise
        """
        return cls.query(cls.name == name).count(1) == 1

    @classmethod
    def create(cls, observacion, name):
        """
        Creates a new nota in the datastore.
        Args:
            - name: String holding the unique name of the nota (app created)
            - observacion: url safe key for the related observacion

        Returns:
            Key of new entity
        """
        try:
            if Nota.exists(name):
                raise NotaCreationError('Nota already exists in platform')
            else:
                o_key = ndb.Key(urlsafe=observacion)
                m = Nota(observacion=o_key, name=name)
                key = m.put()

        except Exception:
            logging.exception("[nota] - Error in create Nota", exc_info=True)
            raise NotaCreationError('Error creating the Nota in platform')
        else:
            return key

    @classmethod
    def get_from_datastore(cls, name):
        """
        Gets a nota from datastore based on its name
        """
        try:
            if Nota.exists(name):
                query = Nota.query(Nota.name == name).fetch(limit=1)
                n = query
            else:
                raise GetNotaError('Nota does not exist')
        except Exception as e:
                raise GetNotaError('Error getting Nota: '+e.__str__())
        else:
            logging.debug("[Nota] - Key = {0}".format(n[0].key))
            logging.debug("[Nota] - Observacion = {0}".format(n[0].observacion))
            logging.debug("[Nota] - name = {0}".format(n[0].name))
            return n[0]



class NotaCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GetNotaError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

