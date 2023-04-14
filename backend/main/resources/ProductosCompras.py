from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ProductoCompraModel

class ProductoCompras(Resource):
    def get(self):
        pagina = 1
        paginado = 2
        productocompras = db.session.query(ProductoCompraModel)
        if request.get_json(silent=True):   #Silent para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina =int(value)
                elif key == 'per_page':
                    paginado = int(value)
        productocompras = productocompras.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page=10)
        return jsonify({
            'productocompras': [productocompra.to_json() for productocompra in productocompras.items],
            'total': productocompras.total,
            'pages': productocompras.pages,
            'pages': pagina
        })
            



    def post(self):
        productocompra = ProductoCompraModel.from_json(request.get_json())
        db.session.add(productocompra)
        db.session.commit()
        return productocompra.to_json(), 201

class ProductosCompra(Resource):
    def get(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            return productocompra.to_json()
        except:
            return '', 404
        
    def delete(self, id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
            return '', 204
        except:
            return '', 404
        
    def put(self,id):
        productocompra = db.session.query(ProductoCompraModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(productocompra, key, value)
        try:
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json(), 201
        except:
            return '', 404
