"""
Defines the datastore and all interfaces needed for a location in the Observador-Electoral platform.
Identifies a place where an observer reported their coordinates.
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb
from observador import Observador


class Location(ndb.Model):
    """
    Represents a place where the Observador reported coordinates within the platform.

        - loc: Geographic coordinates of a location
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    observador = ndb.KeyProperty(kind=Observador)
    loc = ndb.GeoPtProperty()

    @classmethod
    def create(cls, observador, loc):
        """
        Creates a new location in the datastore.
        :param:
            - loc: Geographic coordinates of a location

        :return:
            Key of new entity
        """
        try:
            o = Observador.get_from_datastore(email=observador)
            geo_pt = ndb.GeoPt(str(loc))
            l = Location(loc=geo_pt, observador=o.key)
            key = l.put()

        except Exception:
            logging.exception("[location] - Error in create location", exc_info=True)
            raise LocationCreationError('Error creating the location in platform')
        else:
            return key


class LocationCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


