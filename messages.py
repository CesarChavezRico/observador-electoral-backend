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

