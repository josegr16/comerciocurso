from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoModel
from main.auth.decorators import role_required

class Producto(Resource):
    def get(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            return producto.to_json()
        except:
            return 'Resource not found', 404
        
    @role_required(roles=["admin"])
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)

        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except:
            return '', 404
        
    @role_required(roles=["admin"])
    def delete(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return '', 404


class Productos(Resource):
    
    def get(self):
    
        pagina = 1
        paginado = 2
        productos = db.session.query(ProductoModel)

        if request.get_json(silent=True): #Para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina =int(value)
                elif key == 'per-page':
                    paginatdo = int(value)

        productos = productos.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page = 15)

        return({
            "productos": [producto.to_json() for producto in productos.items],
            "pages": productos.pages,
            "page": pagina
        })

    @role_required(roles=["admin"])
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(), 201