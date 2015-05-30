"""
Defines the datastore and all interfaces needed for a Observador in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb


class Observador(ndb.Model):
    """
    Represents a observador in the platform.

        - account_type: Authentication used to validate the Observador.
        - installation_id: Parse parameter for Push notifications.
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()
    account_type = ndb.StringProperty(choices=['Facebook', 'G+'])
    installation_id = ndb.StringProperty()

    @classmethod
    def exists(cls, email):
        """
        Checks the datastore to find if the observador (email) is already on it.

        Args:
            email: (String) email from request

        Returns:
            True if email exist False otherwise
        """
        return cls.query(cls.email == email).count(1) == 1

    @classmethod
    def create_in_datastore(cls, account_type, age, email, name, installation_id):
        """
        Creates a new observador in datastore
        """
        try:
            if Observador.exists(email):
                raise ObservadorCreationError('Observador email already in platform')
            else:
                o = Observador(account_type=account_type,
                               age=age,
                               email=email,
                               name=name,
                               installation_id=installation_id)
                key = o.put()
        except Exception as e:
            raise ObservadorCreationError('Error creating the user in platform: '+e.__str__())
        else:
            logging.debug('[Observador] - New Observador Key = {0}'.format(key))
            return True

    @classmethod
    def get_from_datastore(cls, email):
        """
        Gets observador from datastore based on email
        """
        try:
            if Observador.exists(email):
                query = Observador.query(Observador.email == email).fetch(limit=1)
                u = query
            else:
                raise GetObservadorError('Observador does not exist')
        except Exception as e:
                raise GetObservadorError('Error getting user: '+e.__str__())
        else:
            logging.debug("[Observador] - Key = {0}".format(u[0].key))
            logging.debug("[Observador] - email = {0}".format(u[0].email))
            logging.debug("[Observador] - name = {0}".format(u[0].name))
            logging.debug("[Observador] - age = {0}".format(u[0].age))
            logging.debug("[Observador] - account_type = {0}".format(u[0].account_type))
            logging.debug("[Observador] - installation_id = {0}".format(u[0].installation_id))
            return u[0]


class ObservadorCreationError(Exception):
    def __init__(self, value):
        self.value = value
        logging.exception('[Observador] - '+value, exc_info=True)

    def __str__(self):
        return repr(self.value)


class GetObservadorError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

