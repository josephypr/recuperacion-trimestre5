from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flaskr.modelos.modelos import db, Usuario, Libro
import cloudinary.uploader
import cloudinary

cloudinary.config(
    cloud_name='dr8dcla9c',
    api_key='462582264781828',
    api_secret='OzfGImdVEAemsNu0ziP3P_2lCy8'
)

rutas = Blueprint('rutas', __name__)

# Validar superadmin
def requiere_superadmin(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        usuario = get_jwt_identity()  # El identity debe ser un string simple
        usuario = Usuario.query.filter_by(correo=usuario).first()  # Obtener el usuario a partir del correo
        if not usuario or usuario.rol != 'superadmin':
            return jsonify({'mensaje': 'No autorizado'}), 403
        return func(*args, **kwargs)
    return wrapper

# Rutas de autenticación
@rutas.route('/autenticacion/registro', methods=['POST'])
def registro():
    datos = request.json
    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    usuario = Usuario(correo=correo)
    usuario.establecer_contrasena(contrasena)
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201


@rutas.route('/autenticacion/login', methods=['POST'])
def login():
    datos = request.json
    correo = datos.get('correo')
    contrasena = datos.get('contrasena')

    usuario = Usuario.query.filter_by(correo=correo).first()
    if not usuario or not usuario.verificar_contrasena(contrasena):
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401

    # Usamos el correo como un string único para el identity
    token = create_access_token(identity=usuario.correo)

    return jsonify({'token': token}), 200


# Rutas de administración
@rutas.route('/admin/gestionar-administradores', methods=['PUT'])
@requiere_superadmin
def gestionar_administradores():
    datos = request.json
    admin_id = datos.get('admin_id')
    accion = datos.get('accion')  # activar/desactivar

    administrador = Usuario.query.get(admin_id)
    if not administrador or administrador.rol != 'admin':
        return jsonify({'mensaje': 'Administrador no encontrado'}), 404

    if accion == 'activar':
        administrador.esta_activo = True
    elif accion == 'desactivar':
        administrador.esta_activo = False
    else:
        return jsonify({'mensaje': 'Acción inválida'}), 400

    db.session.commit()
    return jsonify({'mensaje': f'Administrador {accion} correctamente'})


# Rutas para libros
@rutas.route('/libros/agregar', methods=['POST'])
@jwt_required()
def agregar_libro():
    datos = request.json
    titulo = datos.get('titulo')
    categoria = datos.get('categoria')

    libro = Libro(titulo=titulo, categoria=categoria)
    db.session.add(libro)
    db.session.commit()
    return jsonify({'mensaje': 'Libro agregado correctamente'}), 201


@rutas.route('/libros/subir-imagen/<int:libro_id>', methods=['POST'])
@jwt_required()
def subir_imagen(libro_id):
    libro = Libro.query.get(libro_id)
    if not libro:
        return jsonify({'mensaje': 'Libro no encontrado'}), 404

    archivo = request.files['imagen']
    resultado = cloudinary.uploader.upload(archivo)
    libro.url_imagen = resultado['secure_url']
    db.session.commit()
    return jsonify({'mensaje': 'Imagen subida correctamente', 'url_imagen': libro.url_imagen})
