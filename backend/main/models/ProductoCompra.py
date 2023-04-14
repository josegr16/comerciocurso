from .. import db

class ProductoCompra(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    productoId = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    producto = db.relationship('Producto', back_populates='productoscompras', uselist=False, single_parent=True)
    compraId = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    compra = db.relationship('Compra', back_populates="productoscompras", uselist=False, single_parent=True)

    def __repr__(self):
        return f'Producto-Compras: {self.producto.to_json()}'

    def to_json(self):
        productoCompra_json = {
            'id': self.id,
            'producto': self.producto.to_json(),
            'compra': self.compra.to_json()
        }
        return productoCompra_json

    @staticmethod
    def from_json(productocompra_json):
        id = productocompra_json.get('id')
        productoId = productocompra_json.get('productoId')
        compraId = productocompra_json.get('compraId')
        return ProductoCompra(
            id = id,
            productoId = productoId,
            compraId = compraId
        )