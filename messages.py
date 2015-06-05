"""
Defined here are the ProtoRPC message class definitions for the API.
"""
__author__ = 'Cesar'


from protorpc import messages


"""
OBSERVADOR
"""

class CreateObservador(messages.Message):
    """
    Message containing the information of a User
        email: (String)
        name: (String)
        age: (Integer)
        account_type: (String)
        installation_id: (String) Parse ID for Push notifications
    """
    email = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)
    age = messages.IntegerField(3)
    account_type = messages.StringField(4, required=True)
    installation_id = messages.StringField(5, required=True)


class CreateObservadorResponse(messages.Message):
    """
    Response to user creation request
        ok: (Boolean) User creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)


class GetObservador(messages.Message):
    """
    Message containing the information of a observador
        email: (String)
    """
    email = messages.StringField(1, required=True)


class GetObservadorResponse(messages.Message):
    """
    Response to observador information request
        ok: (Boolean) User search successful or failed
        error: (String) If search failed, contains the reason, otherwise empty.

        email = (String)
        name = (String)
        age = (Integer)
        account_type = (String)
        installation_id = (String) Parse ID for Push notifications
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)

    email = messages.StringField(3)
    name = messages.StringField(4)
    age = messages.IntegerField(5)
    account_type = messages.StringField(6)
    installation_id = messages.StringField(7)

"""
CASILLA
"""

class CreateCasilla(messages.Message):
    """
    Message containing the information of a Casilla
        national_id: (String) unique identifier of the Casilla in the national database
        distrito: (String) unique identifier of the Distrito this casilla belongs to
        name: (String)
    """
    national_id = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)
    loc = messages.StringField(3, required=True)
    address = messages.StringField(4, required=True)
    picture_url = messages.StringField(5, required=True)
    distrito = messages.StringField(6, required=True)


class CreateCasillaResponse(messages.Message):
    """
    Response to casilla creation request
        ok: (Boolean) Casilla creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)


class Casilla(messages.Message):
    """
    Casilla entity for details response
    """
    observador = messages.StringField(1)
    distrito = messages.StringField(2)
    national_id = messages.StringField(3)
    loc = messages.StringField(4)
    name = messages.StringField(5)
    address = messages.StringField(6)
    picture_url = messages.StringField(7)


class GetCasillaDetail(messages.Message):
    """
    Message requesting the detail for a given casilla
        casilla: national id

    """
    casilla = messages.StringField(1, required=True)



class GetCasillaDetailResponse(messages.Message):
    """
    Response to Casilla detail request.
        ok: (Boolean)
        Casilla (JSON): Casilla details
        error: (String) If request failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    casilla = messages.MessageField(Casilla, 2)
    error = messages.StringField(3)


class AssignCasillaToObservador(messages.Message):
    """
    Message to assign a casilla to a observador
        casilla: national_id key for the casilla
        observador: email

    """
    casilla = messages.StringField(1, required=True)
    observador = messages.StringField(2, required=True)



class AssignCasillaToObservadorResponse(messages.Message):
    """
    Response to Casilla detail request.
        ok: (Boolean)
        error: (String) If request failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)


"""
DISTRITO
"""

class CreateDistrito(messages.Message):
    """
    Message containing the information of a Distrito
        national_id: (String) unique identifier of the Casilla in the national database
        name: (String)
    """
    national_id = messages.StringField(1, required=True)
    name = messages.StringField(2, required=True)


class CreateDistritoResponse(messages.Message):
    """
    Response to distrito creation request
        ok: (Boolean) Distrito creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)


"""
OBSERVACION
"""

class CreateObservacion(messages.Message):
    """
    Message containing the information of a Observacion
        casilla: national_id
        observador: email
        media: file name
        nota: file name
    """
    casilla = messages.StringField(1, required=True)
    observador = messages.StringField(2, required=True)
    clasificacion = messages.StringField(3, required=True)
    filled_checklist = messages.StringField(4, required=True)


class CreateObservacionResponse(messages.Message):
    """
    Response to observacion creation request
        ok: (Boolean) Observacion creation successful or failed
        url_safe_key: (String) If creation successful the url safe key of the new observacion
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    url_safe_key = messages.StringField(2)
    error = messages.StringField(3)

"""
MEDIA
"""

class CreateMedia(messages.Message):
    """
    Message containing the information of a new Media
        name: unique name of the media in the bucket. App created
        observacion: url safe key of the observacion
        m_type: type of media [video, photo, audio]

    """
    name = messages.StringField(1, required=True)
    observacion = messages.StringField(2, required=True)
    m_type = messages.StringField(3, required=True)



class CreateMediaResponse(messages.Message):
    """
    Response to media creation request
        ok: (Boolean) Media creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)

"""
NOTA
"""

class CreateNota(messages.Message):
    """
    Message containing the information of a new Nota
        name: unique name of the media in the bucket. App created
        observacion: url safe key of the observacion

    """
    name = messages.StringField(1, required=True)
    observacion = messages.StringField(2, required=True)



class CreateNotaResponse(messages.Message):
    """
    Response to nota creation request
        ok: (Boolean) Nota creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)

"""
LOCATION
"""

class CreateLocation(messages.Message):
    """
    Message containing the information of a Location
        loc: coordinates
        observador: email

    """
    loc = messages.StringField(1, required=True)
    observador = messages.StringField(2, required=True)



class CreateLocationResponse(messages.Message):
    """
    Response to location creation request
        ok: (Boolean) Location creation successful or failed
        casilla_near: (String) URL safe key of a casilla if one is close enough
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    casilla_near = messages.StringField(2)
    error = messages.StringField(3)

"""
CLASIFICACION
"""

class CreateClasificacion(messages.Message):
    """
    Message containing the information of a Clasificacion
        - name: String holding the name of the Clasificacion
        - checklist: JSON string of the checklist to fill for this Clasificacion
        - repeatable: Can only be performed once for a given Casilla

    """
    name = messages.StringField(1, required=True)
    checklist = messages.StringField(2, required=True)
    repeatable = messages.BooleanField(3, required=True)



class CreateClasificacionResponse(messages.Message):
    """
    Response to clasificacion creation request
        ok: (Boolean) Clasificacion creation successful or failed
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    error = messages.StringField(2)


class GetAvailableClasificaciones(messages.Message):
    """
    Message requesting the available clasificaciones for a given casilla
        casilla: national_id (String) unique identifier of the Casilla in the national database

    """
    casilla = messages.StringField(1, required=True)



class GetAvailableClasificacionesResponse(messages.Message):
    """
    Response to available clasificaciones request. Contains the URL safe keys of the available clasificaciones
        ok: (Boolean) Location creation successful or failed
        clasificacion (String): An available clasificacion for the requested casilla
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    clasificacion = messages.StringField(2, repeated=True)
    error = messages.StringField(3)


class GetAllClasificaciones(messages.Message):
    """
    Message requesting all the clasificaciones of the platform

    """



class GetAllClasificacionesResponse(messages.Message):
    """
    Response to all clasificaciones request. Contains the URL safe keys of the clasificaciones
        ok: (Boolean) Location creation successful or failed
        clasificacion (String): A clasificacion
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    clasificacion = messages.StringField(2, repeated=True)
    error = messages.StringField(3)


class Clasificacion(messages.Message):
    """
    Clasificacion entity for details response
    """
    name = messages.StringField(1)
    checklist = messages.StringField(2)
    repeatable = messages.BooleanField(3)


class GetClasificacionDetails(messages.Message):
    """
    Message requesting the details of a given clasificacion
        clasificacion: url_safe_key (String) of the desired clasificacion

    """
    clasificacion = messages.StringField(1, required=True)


class GetClasificacionDetailsResponse(messages.Message):
    """
    Response to clasificacion details request.
        ok: (Boolean) Location creation successful or failed
        clasificacion (JSON): Details of a Clasificacion
        error: (String) If creation failed, contains the reason, otherwise empty.
    """
    ok = messages.BooleanField(1)
    clasificacion = messages.MessageField(Clasificacion, 2)
    error = messages.StringField(3)
