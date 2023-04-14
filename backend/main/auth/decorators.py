from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):
            #Verificar que el JWT es correcto
            verify_jwt_in_request()
            #Obtenemos los claims(peticiones), que estan dentro del JWT
            claims = get_jwt()

            if claims['sub']['role'] in roles:
                return function(*args, **kwargs)
            else:
                return 'rol not allowed', 403
        return wrapper
    return decorator

#decoradores que ya trae el jwt, pero los modificamos, redefinimos
@jwt.user_identity_loader
def user_identify_lookup(usuario):
    return{
        'usuarioId': usuario.id,
        'role': usuario.role
    }

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'id': usuario.id,
        'role': usuario.role,
        'email': usuario.email
    }