from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.types import Enum
from flask_sqlalchemy import SQLAlchemy
from flaskr import db




class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contrasena = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(50), default='admin')  # superadmin, admin, user
    esta_activo = db.Column(db.Boolean, default=True)
    foto_perfil = db.Column(db.String(250), nullable=True)

    def establecer_contrasena(self, contrasena):
        self.contrasena = generate_password_hash(contrasena).decode('utf-8')

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena, contrasena)



class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(250), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    estado = db.Column(Enum('disponible', 'prestado', 'reservado', name='estado_libro'), default='disponible')
    url_imagen = db.Column(db.String(250), nullable=True)


# serializacion
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

    @post_load
    def encriptar_contrasena(self, data, **kwargs):
        if 'contrasena' in data:
            data['contrasena'] = generate_password_hash(data['contrasena']).decode('utf-8')
        return data



class LibroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Libro
        include_relationships = True
        load_instance = True
