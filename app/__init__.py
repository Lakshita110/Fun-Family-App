from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
# from flask_session import Session 

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# sess = Session()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        # from .models import 
        db.create_all()
        login_manager.init_app(app)
        # sess.init_app(app)   

    from app.auth.routes import auth
    # from app.quiz.routes import quiz
    app.register_blueprint(auth) 

    return app

app = create_app()
