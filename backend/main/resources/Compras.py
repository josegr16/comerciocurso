from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModel
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity


class Compra(Resource):

    @role_required(roles=["admin", "cliente"])
    def get(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == 'admin':
            try:
                return compra.to_json()
            except:
                return '', 404
        else:
            return 'Unauthorized', 401
        
    @role_required(roles=["admin", "cliente"])
    def put (self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == 'admin':
            data = request.get_json().items()
            for key, value in data:
                setattr(compra, key, value)
            try:
                db.session.add(compra)
                db.session.commit()
                return compra.to_json(), 201
            except:
                return '', 404
        else:
            return 'Unauthorized', 401

    @role_required(roles=["admin", "cliente"])
    def delete(self, id):
        compra = db.session.query(CompraModel).get_or_404(id)
        current_user = get_jwt_identity()
        if current_user['usuarioId'] == compra.usuarioId or current_user['role'] == 'admin':
            try:
                db.session.delete(compra)
                db.session.commit()
                return '', 204
            except:
                return '', 404
        else:
            return 'Unauthorized', 401



class Compras(Resource):
    def get(self):
        pagina = 1
        paginado = 2
        compras = db.session.query(CompraModel)
        if request.get_json(silent=True):   #Silent para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina =int(value)
                elif key == 'per_page':
                    paginado = int(value)
        compras = compras.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page=10)
        return jsonify({
            'compras': [compra.to_json() for compra in compras.items],
            'total': compras.total,
            'pages': compras.pages,
            'pages': pagina
        })
            
    @role_required(roles=["admin", "cliente"])
    def post(self):
        compra = CompraModel.from_json(request.get_json())
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(), 201