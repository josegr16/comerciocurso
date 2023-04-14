from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel

class Usuario(Resource):
    
    def get(self, id):
        usuario = db.sessio.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    
    def delete(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    def put(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 204


class Usuarios(Resource):
    def get(self):
        pagina = 1
        paginado = 5
        usuarios = db.session.query(UsuarioModel)
        if request.get_json(silent=True):   #Silent para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina =int(value)
                elif key == 'per_page':
                    paginado = int(value)
        usuarios = usuarios.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page=10)
        return jsonify({
            'usuarios': [usuario.to_json() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'pages': pagina
        })

        usuarios = db.session.query(UsuarioModel)
