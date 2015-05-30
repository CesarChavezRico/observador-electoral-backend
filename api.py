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

package = 'OCR'


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
        logging.debug("[FrontEnd] - casilla name = {0}".format(request.name))
        logging.debug("[FrontEnd] - loc = {0}".format(request.loc))
        logging.debug("[FrontEnd] - address = {0}".format(request.address))
        logging.debug("[FrontEnd] - picture_url = {0}".format(request.picture_url))

        resp = messages.CreateCasillaResponse()
        try:
            Casilla.create(loc=request.loc,
                           name=request.name,
                           address=request.address,
                           picture_url=request.picture_url)
        except CasillaCreationError as e:
            resp.error = e.value
        else:
            resp.ok = True
        return resp


app = endpoints.api_server([ObservadorElectoralBackendApi])
