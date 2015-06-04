"""
Defines the datastore and all interfaces needed for a Distrito in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb


class Distrito(ndb.Model):
    """
    Represents a distrito within the platform.

        - national_id: Unique national_id for the distrito in the national database
        - name:
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    national_id = ndb.StringProperty()
    name = ndb.StringProperty()

    @classmethod
    def exists(cls, national_id):
        """
        Checks the datastore to find if the distrito (national_id) is already on it.

        Args:
            national_id: (String) national_id from request

        Returns:
            True if national_id exist False otherwise
        """
        return cls.query(cls.national_id == national_id).count(1) == 1

    @classmethod
    def create(cls, national_id, name):
        """
        Creates a new distrito in the datastore.
        Args:
            - unique national_id: String holding the unique national_id for the distrito in the national database
            - name: String holding the name of the distrito

        Returns:
            Key of new entity
        """
        try:
            if Distrito.exists(national_id):
                raise DistritoCreationError('Distrito already in platform')
            else:
                d = Distrito(national_id=national_id, name=name)
                key = d.put()

        except Exception:
            logging.exception("[distrito] - Error in create Distrito", exc_info=True)
            raise DistritoCreationError('Error creating the Distrito in platform')
        else:
            return key

    @classmethod
    def get_from_datastore(cls, national_id):
        """
        Gets a distrito from datastore based on its unique national_id (from national database)
        """
        try:
            if Distrito.exists(national_id):
                query = Distrito.query(Distrito.national_id == national_id).fetch(limit=1)
                u = query
            else:
                raise GetDistritoError('Distrito does not exist')
        except Exception as e:
                raise GetDistritoError('Error getting Distrito: '+e.__str__())
        else:
            logging.debug("[Distrito] - Key = {0}".format(u[0].key))
            logging.debug("[Distrito] - national_id = {0}".format(u[0].national_id))
            logging.debug("[Distrito] - name = {0}".format(u[0].name))
            return u[0]



class DistritoCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GetDistritoError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

