"""
Defines all methods needed for the API. Implemented using Google Cloud Endpoints.
"""

__author__ = 'Cesar'

import endpoints
from protorpc import remote
import logging
import messages
from observador import Observador, ObservadorCreationError, GetObservadorError
from casilla import Casilla, CasillaCreationError, GetCasillaError
from distrito import Distrito, DistritoCreationError
from observacion import Observacion, ObservacionCreationError
from location import Location, LocationCreationError
from media import Media, MediaCreationError
from nota import Nota, NotaCreationError
from clasificacion import Clasificacion, GetClasificacionError, ClasificacionCreationError

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

    @endpoints.method(messages.GetCasillaDetail,
                      messages.GetCasillaDetailResponse,
                      http_method='POST',
                      name='casilla.get',
                      path='casilla/get')
    def get_casilla(self, request):
        """
        Gets the details of a given casilla national_id.
        """
        logging.debug("[FrontEnd] - get_casilla_details - Casilla: {0}".format(request.casilla))
        resp = messages.GetCasillaDetailResponse()
        try:
            r = Casilla.get_from_datastore(request.casilla)
            r_c = messages.Casilla()

            if r.observador:
                r_c.observador = r.observador.urlsafe()
            else:
                r_c.observador = 'Observador no Asignado'
            r_c.distrito = r.distrito.urlsafe()
            r_c.national_id = r.national_id
            r_c.loc = str(r.loc)
            r_c.name = r.name
            r_c.address = r.address
            r_c.picture_url = r.picture_url

            resp.casilla = r_c
        except GetClasificacionError as e:
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
        logging.debug("[FrontEnd] - Observacion - Clasificacion = {0}".format(request.clasificacion))
        logging.debug("[FrontEnd] - Observacion - Filled Checklist = {0}".format(request.filled_checklist))

        resp = messages.CreateObservacionResponse()
        try:
            url_safe_key = Observacion.save_to_datastore(casilla=request.casilla,
                                                         observador=request.observador,
                                                         clasificacion=request.clasificacion,
                                                         filled_checklist=request.filled_checklist)
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
            try:
                # Find a near casilla
                c = Casilla.get_based_on_location(request.loc, 10)
            except GetCasillaError as e:
                resp.error = e.value
            else:
                resp.casilla_near = c.key.urlsafe()
            resp.ok = True
        return resp

    """
    CLASIFICACION
    """
    @endpoints.method(messages.CreateClasificacion,
                      messages.CreateClasificacionResponse,
                      http_method='POST',
                      name='clasificacion.create',
                      path='clasificacion/create')
    def new_clasificacion(self, request):
        """
        Generates a new clasificacion in the platform.
        """
        logging.debug("[FrontEnd] - Clasificacion - Name = {0}".format(request.name))
        logging.debug("[FrontEnd] - Clasificacion - Checklist = {0}".format(request.checklist))
        logging.debug("[FrontEnd] - Clasificacion - Repeatable = {0}".format(request.repeatable))

        resp = messages.CreateClasificacionResponse()
        try:
            Clasificacion.create(name=request.name, checklist=request.checklist, repeatable=request.repeatable)
        except ClasificacionCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    @endpoints.method(messages.GetAvailableClasificaciones,
                      messages.GetAvailableClasificacionesResponse,
                      http_method='POST',
                      name='clasificacion.get_available',
                      path='clasificacion/get_available')
    def get_clasificaciones(self, request):
        """
        Gets all the available clasificaciones for a given Casilla.
        """
        logging.debug("[FrontEnd] - Get Available Clasificaciones - Casilla = {0}".format(request.casilla))
        resp = messages.GetAvailableClasificacionesResponse()
        try:
            resp.clasificacion = Clasificacion.get_available(request.casilla)
        except GetClasificacionError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    @endpoints.method(messages.GetAllClasificaciones,
                      messages.GetAllClasificacionesResponse,
                      http_method='POST',
                      name='clasificacion.get_all',
                      path='clasificacion/get_all')
    def get_all_clasificaciones(self, request):
        """
        Gets all clasificaciones.
        """
        logging.debug("[FrontEnd] - Get All Clasificaciones")
        resp = messages.GetAllClasificacionesResponse()
        try:
            resp.clasificacion = Clasificacion.get_all()
        except GetClasificacionError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

    @endpoints.method(messages.GetClasificacionDetails,
                      messages.GetClasificacionDetailsResponse,
                      http_method='POST',
                      name='clasificacion.get_detail',
                      path='clasificacion/get_detail')
    def get_clasificacion_details(self, request):
        """
        Gets the details of a given clasificacion.
        """
        logging.debug("[FrontEnd] - get_clasificacion_details - Clasificacion: {0}".format(request.clasificacion))
        resp = messages.GetClasificacionDetailsResponse()
        try:
            r = Clasificacion.get_details(request.clasificacion)
            r_c = messages.Clasificacion()
            r_c.name = r.name
            r_c.checklist = r.checklist
            r_c.repeatable = r.repeatable
            resp.clasificacion = r_c
        except GetClasificacionError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp

app = endpoints.api_server([ObservadorElectoralBackendApi])
