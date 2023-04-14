from flask import request, Blueprint
from .. import db
from main.models import UsuarioModel
from flask_jwt_extended import create_access_token
from main.auth.decorators import user_identify_lookup
from main.mail.functions import send_mail

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    #Buscamos al usuario en la db mediante el email
    usuario = db.session.query(UsuarioModel).filter(UsuarioModel.email == request.get_json().get('email')).first_or_404()

    #Validamos la contraseña de ese usuario
    if usuario.validate_pass(request.get_json().get("password")):
        #Generamos un nuevo token y le pasamos al usuario como identidad de ese token
        access_token = create_access_token(identity=usuario)

        #devolvemos los valores y el token
        data = {
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token,
            'role': str(usuario.role)
        }
        return data, 200
    else:
        return 'Incorrect password', 401


@auth.route('/register', methods=['POST'])
def register():
    usuario = UsuarioModel.from_json(request.get_json())
    exits = db.session.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).scalar() is not None
    if exits:
        return 'Duplicate email', 409
    else: 
        try:
            db.session.add(usuario)
            db.session.commit()
            send_mail([usuario.email], "Bienvenido", 'register', usuario = usuario)
        except Exception as error:
            db.session.rollback()
            return str(error), 409
        return usuario.to_json(), 201