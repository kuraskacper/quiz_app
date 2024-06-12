from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_login import LoginManager

db = SQLAlchemy()
DB_USER_NAME = 'quiz'
DB_PASSWORD = 'Kacper/12'
DB_HOST_NAME = 'localhost'
DB_NAME = 'quiz_app'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST_NAME}/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth)

    from . import models

    with app.app_context():
        database_create(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app


def database_create(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
        print('Created Database!')
    db.create_all()
