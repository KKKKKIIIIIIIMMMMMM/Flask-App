from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from kim_gallery.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from kim_gallery.main import bp as main_bp
    app.register_blueprint(main_bp)

    from kim_gallery.gallery import bp as gallery_bp
    app.register_blueprint(gallery_bp)

    return app
