from .. import db

class Producto(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    productoscompras = db.relationship('ProductoCompra', back_populates='producto', cascade="all, delete-orphan")

    def __repr__(self):
        return f'Producto: {self.nombre}'

    def to_json(self):  
        producto_json = {
        'id': self.id,
        'nombre': self.nombre,
        'precio': self.precio,
        'imagen': self.imagen,
        'descripcion': self.descripcion,
        'stock': self.stock
        }
        return producto_json

    @staticmethod
    def from_json(producto_json):
        id = producto_json.get ('id')
        nombre = producto_json.get ('nombre')
        precio = producto_json.get ('precio')
        imagen = producto_json.get ('imagen')
        descripcion = producto_json.get ('descripcion')
        stock = producto_json.get ('stock')
        return Producto(
            id = id,
            nombre = nombre,
            precio = precio,
            imagen = imagen,
            descripcion = descripcion,
            stock = stock
            )

