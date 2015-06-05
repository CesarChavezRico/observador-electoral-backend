"""
Defines the datastore and all interfaces needed for a Media in the Observador-Electoral platform
"""
__author__ = 'Cesar'


import logging
from google.appengine.ext import ndb
from observacion import Observacion


class Media(ndb.Model):
    """
    Represents a media within the platform.

        - observacion:
        - m_type: type of media [video, photo, audio]
        - name: unique id for media file in bucket
    """

    created = ndb.DateTimeProperty(auto_now_add=True)
    observacion = ndb.KeyProperty(kind=Observacion)
    m_type = ndb.StringProperty(choices=['video', 'photo', 'audio'])
    name = ndb.StringProperty()

    @classmethod
    def exists(cls, name):
        """
        Checks the datastore to find if the media (name) is already on it.

        Args:
            name: (String) name from request

        Returns:
            True if name exist False otherwise
        """
        return cls.query(cls.name == name).count(1) == 1

    @classmethod
    def create(cls, m_type, name, observacion):
        """
        Creates a new media in the datastore.
        Args:
            - observacion: URL safe key of the related observacion
            - m_type: String holding the type for media
            - name: String holding the unique name of the media (app created)

        Returns:
            Key of new entity
        """
        try:
            if Media.exists(name):
                raise MediaCreationError('Media already exists in platform')
            else:
                o_key = ndb.Key(urlsafe=observacion)
                m = Media(observacion=o_key, m_type=m_type, name=name)
                key = m.put()

        except Exception:
            logging.exception("[media] - Error in create Media", exc_info=True)
            raise MediaCreationError('Error creating the Media in platform')
        else:
            return key

    @classmethod
    def get_from_datastore(cls, name):
        """
        Gets a media from datastore based on its name
        """
        try:
            if Media.exists(name):
                query = Media.query(Media.name == name).fetch(limit=1)
                m = query
            else:
                raise GetMediaError('Media does not exist')
        except Exception as e:
                raise GetMediaError('Error getting Media: '+e.__str__())
        else:
            logging.debug("[Media] - Key = {0}".format(m[0].key))
            logging.debug("[Media] - Observacion = {0}".format(m[0].observacion))
            logging.debug("[Media] - type = {0}".format(m[0].type))
            logging.debug("[Media] - name = {0}".format(m[0].name))
            return m[0]



class MediaCreationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GetMediaError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

