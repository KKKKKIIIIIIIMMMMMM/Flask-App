from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Import and register blueprints
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from image import image as image_blueprint
    app.register_blueprint(image_blueprint)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)