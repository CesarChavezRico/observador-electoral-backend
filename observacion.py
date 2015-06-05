"""
Defines the datastore and all interfaces needed for a Observacion in the platform
"""
__author__ = 'Cesar'

import logging
from google.appengine.ext import ndb
from casilla import Casilla
from observador import Observador
from clasificacion import Clasificacion


class Observacion(ndb.Model):
    """
    Represents a observacion of a Casilla in the platform.

        - observador: Author of this Observacion
        - casilla: The casilla the Observacion is about
        - clasificacion: The clasificacion related to this Observacion
        - filled_checklist: The Observador filled checklist for this Observacion (the checklist template should
          come from the associated Clasificacion)
    """

    date = ndb.DateTimeProperty(auto_now_add=True)
    casilla = ndb.KeyProperty(kind=Casilla)
    observador = ndb.KeyProperty(kind=Observador)
    clasificacion = ndb.KeyProperty(kind=Clasificacion)
    filled_checklist = ndb.JsonProperty()

    @classmethod
    def save_to_datastore(cls, observador, casilla, clasificacion, filled_checklist):
        """
        Saves a Observacion as a new entity on the datastore.
            :param observador: (String) email
            :param casilla: (String) national id
            :param clasificacion: URL safe key of the Observador selected clasificacion
            :param filled_checklist: JSON of checklist filled by the Observador


            :return key: If creation successful URL safe key of the new observacion, exception otherwise
        """
        try:
            c = Casilla.get_from_datastore(casilla)
            o = Observador.get_from_datastore(observador)
            new = Observacion(casilla=c.key,
                              observador=o.key,
                              clasificacion=ndb.Key(urlsafe=clasificacion),
                              filled_checklist=filled_checklist)
            key = new.put()
        except Exception as e:
            logging.exception("[Observacion] - "+e.message)
            raise ObservacionCreationError('Error creating the observacion in datastore: '+e.__str__())
        else:
            logging.debug('[Observacion] - New Observacion, Key = {0}'.format(key))
            return key.urlsafe()

    @classmethod
    def get_all(cls, casilla):
        """
        Gets all the observaciones for a given casilla
            :param casilla:
            :return: list of all observaciones

        """
        try:
            observaciones = []
            c = Casilla.get_from_datastore(casilla)
            query_response = Observacion.query(Observacion.casilla == c.key).fetch()
            if query_response:
                for r in query_response:
                    observaciones.append(r)
            else:
                raise GetObservacionError('No Observaciones found under specified criteria: Casilla: {0}'
                                          .format(casilla))
        except Exception as e:
            logging.exception("[Observacion] - "+e.message)
            raise GetObservacionError('Error getting Observaciones: '+e.__str__())
        else:
            for r in observaciones:
                logging.debug("[Observacion] = {0}".format(r))
            return observaciones

    @classmethod
    def count(cls):
        """
        Gets the total number of observaciones
            :return: number

        """
        try:
            query_response = Observacion.query()
            number = query_response.count()
            if number > 0:
                pass
            else:
                raise GetObservacionError('No Observaciones found')
        except Exception as e:
            logging.exception("[Observacion] - "+e.message)
            raise GetObservacionError('Error getting Observaciones: '+e.__str__())
        else:
            return number


class ObservacionCreationError(Exception):
    def __init__(self, value):
        self.value = value
        logging.exception('[Observacion] - Observacion Error:'+value, exc_info=True)

    def __str__(self):
        return repr(self.value)


class GetObservacionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
