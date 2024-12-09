from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Instancias globales
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'tu_secreto_aqui'

    
    db.init_app(app)
    jwt.init_app(app)

    # Registrar el Blueprint
    from flaskr.vistas import rutas
    app.register_blueprint(rutas)

    # Crear tablas y superadmin
    with app.app_context():
        db.create_all()
        from flaskr.modelos.modelos import Usuario
        if not Usuario.query.filter_by(rol='superadmin').first():
            superadmin = Usuario(correo='superadmin@ejemplo.com')
            superadmin.establecer_contrasena('123456')
            superadmin.rol = 'superadmin'
            db.session.add(superadmin)
            db.session.commit()

    return app
