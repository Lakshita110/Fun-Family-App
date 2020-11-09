from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        login_manager.init_app(app)  

    from app.auth.routes import auth    
    app.register_blueprint(auth) 
    from app.lists.routes import lists
    app.register_blueprint(lists)

    return app

app = create_app()
