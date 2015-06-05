"""
Defines all methods needed for the API. Implemented using Google Cloud Endpoints.
"""

__author__ = 'Cesar'

import endpoints
from protorpc import remote
import logging
import messages
from observador import Observador, ObservadorCreationError, GetObservadorError
from casilla import Casilla, CasillaCreationError
from distrito import Distrito, DistritoCreationError
from observacion import Observacion, ObservacionCreationError
from location import Location, LocationCreationError
from media import Media, MediaCreationError
from nota import Nota, NotaCreationError

package = 'ObservadorElectoral'


@endpoints.api(name='backend', version='v1', hostname='observador-electoral.appspot.com')
class ObservadorElectoralBackendApi(remote.Service):
    """
    Observador Electoral Backend Services
    """

    """
    OBSERVADOR
    """
    @endpoints.method(messages.CreateObservador,
                      messages.CreateObservadorResponse,
                      http_method='POST',
                      name='observador.create',
                      path='observador/create')
    def new_observador(self, request):
        """
        Generates a new observador in the platform, if the email is already in use returns an error
        """
        logging.debug("[FrontEnd - new_observador()] - email = {0}".format(request.email))
        logging.debug("[FrontEnd - new_observador()] - name = {0}".format(request.name))
        logging.debug("[FrontEnd - new_observador()] - age = {0}".format(request.age))
        logging.debug("[FrontEnd - new_observador()] - account_type = {0}".format(request.account_type))
        logging.debug("[FrontEnd - new_observador()] - installation_id = {0}".format(request.installation_id))
        resp = messages.CreateObservadorResponse()
        try:
            Observador.create_in_datastore(email=request.email,
                                           name=request.name,
                                           age=request.age,
                                           account_type=request.account_type,
                                           installation_id=request.installation_id)
        except ObservadorCreationError as e:
            resp.ok = False
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    @endpoints.method(messages.GetObservador,
                      messages.GetObservadorResponse,
                      http_method='POST',
                      name='observador.get',
                      path='observador/get')
    def get_observador(self, request):
        """
        Gets a observador information based on it's email address
        """
        logging.debug("[FrontEnd - get_observador()] - email = {0}".format(request.email))
        resp = messages.GetObservadorResponse()
        try:
            retrieved_observador = Observador.get_from_datastore(email=request.email)
            resp.email = retrieved_observador.email
            resp.name = retrieved_observador.name
            resp.age = retrieved_observador.age
            resp.account_type = retrieved_observador.account_type
            resp.installation_id = retrieved_observador.installation_id
        except GetObservadorError as e:
            resp.ok = False
            resp.error = e.value
        except Exception as e:
            resp.ok = False
            resp.error = e.message

        else:
            resp.ok = True
        return resp

    """
    CASILLA
    """
    @endpoints.method(messages.CreateCasilla,
                      messages.CreateCasillaResponse,
                      http_method='POST',
                      name='casilla.create',
                      path='casilla/create')
    def new_casilla(self, request):
        """
        Generates a new casilla in the platform.
        """
        logging.debug("[FrontEnd] - Casilla - national id = {0}".format(request.national_id))
        logging.debug("[FrontEnd] - Distrito - national id = {0}".format(request.distrito))
        logging.debug("[FrontEnd] - casilla name = {0}".format(request.name))
        logging.debug("[FrontEnd] - loc = {0}".format(request.loc))
        logging.debug("[FrontEnd] - address = {0}".format(request.address))
        logging.debug("[FrontEnd] - picture_url = {0}".format(request.picture_url))

        resp = messages.CreateCasillaResponse()
        try:
            Casilla.create(loc=request.loc,
                           name=request.name,
                           address=request.address,
                           picture_url=request.picture_url,
                           national_id=request.national_id,
                           distrito=request.distrito)
        except CasillaCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    """
    DISTRITO
    """
    @endpoints.method(messages.CreateDistrito,
                      messages.CreateDistritoResponse,
                      http_method='POST',
                      name='distrito.create',
                      path='distrito/create')
    def new_distrito(self, request):
        """
        Generates a new distrito in the platform.
        """
        logging.debug("[FrontEnd] - Distrito - national id = {0}".format(request.national_id))
        logging.debug("[FrontEnd] - Distrito name = {0}".format(request.name))

        resp = messages.CreateDistritoResponse()
        try:
            Distrito.create(name=request.name,
                            national_id=request.national_id)
        except DistritoCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    """
    OBSERVACION
    """
    @endpoints.method(messages.CreateObservacion,
                      messages.CreateObservacionResponse,
                      http_method='POST',
                      name='observacion.create',
                      path='observacion/create')
    def new_observacion(self, request):
        """
        Generates a new observacion in the platform.
        """
        logging.debug("[FrontEnd] - Observacion - Casilla national id = {0}".format(request.casilla))
        logging.debug("[FrontEnd] - Observacion - Observador = {0}".format(request.observador))

        resp = messages.CreateObservacionResponse()
        try:
            url_safe_key = Observacion.save_to_datastore(casilla=request.casilla,
                                                         observador=request.observador)
        except ObservacionCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
            resp.url_safe_key = url_safe_key
        return resp

    """
    MEDIA
    """
    @endpoints.method(messages.CreateMedia,
                      messages.CreateMediaResponse,
                      http_method='POST',
                      name='media.create',
                      path='media/create')
    def new_media(self, request):
        """
        Generates a new media in the platform.
        """
        logging.debug("[FrontEnd] - Media - Name = {0}".format(request.name))
        logging.debug("[FrontEnd] - Media - Observacion = {0}".format(request.observacion))
        logging.debug("[FrontEnd] - Media - Type = {0}".format(request.m_type))

        resp = messages.CreateMediaResponse()
        try:
            Media.create(observacion=request.observacion, name=request.name, m_type=request.m_type)
        except MediaCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    """
    NOTA
    """
    @endpoints.method(messages.CreateNota,
                      messages.CreateNotaResponse,
                      http_method='POST',
                      name='nota.create',
                      path='nota/create')
    def new_nota(self, request):
        """
        Generates a new nota in the platform.
        """
        logging.debug("[FrontEnd] - Nota - Name = {0}".format(request.name))
        logging.debug("[FrontEnd] - Nota - Observacion = {0}".format(request.observacion))

        resp = messages.CreateNotaResponse()
        try:
            Nota.create(observacion=request.observacion, name=request.name)
        except NotaCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    """
    LOCATION
    """
    @endpoints.method(messages.CreateLocation,
                      messages.CreateLocationResponse,
                      http_method='POST',
                      name='location.create',
                      path='location/create')
    def new_location(self, request):
        """
        Generates a new location in the platform.
        """
        logging.debug("[FrontEnd] - Observacion - Observador = {0}".format(request.observador))
        logging.debug("[FrontEnd] - Observacion - Loc = {0}".format(request.loc))

        resp = messages.CreateLocationResponse()
        try:
            Location.create(observador=request.observador, loc=request.loc)
        except LocationCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp


app = endpoints.api_server([ObservadorElectoralBackendApi])
