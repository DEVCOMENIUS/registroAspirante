from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # IMPORTANTE: Importar modelos AQUÍ después de db.init_app pero antes de user_loader
    from app.models.usuario import Usuario
    from app.models.aspirante import Aspirante
    from app.models.docente import Docente
    from app.models.directivo import Directivo
    
    # Definir user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # 👇 ELIMINA ESTA LÍNEA DUPLICADA: from app.models import usuario
    # from app.models import usuario  <--- BORRAR ESTA LÍNEA
    
    from app.controllers.auth_controller import auth_bp
    from app.controllers.registro_controller import registro_bp
    from app.controllers.pdf_controller import pdf_bp
    from app.controllers.inicio_controller import inicio_bp
    from app.controllers.admin_controller import admin_bp
    from app.controllers.docente_controller import docente_bp
    from app.controllers.directivo_controller import directivo_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(inicio_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(directivo_bp)


    return app