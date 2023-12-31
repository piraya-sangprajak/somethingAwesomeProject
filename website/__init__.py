from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path # os (operating system)
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # encrypt or secure the cookie and session data related to our website
    app.config['SECRET_KEY'] = 'cookie yumyum njkbc$%$E56wsfn'
    # store the database in our website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import our Blueprint
    from .views import views
    from .auth import auth

    # register our Blueprint with Flask
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # make sure models.py file runs before creating the database
    from .models import User, Note
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # looks for user using ID
        return User.query.get(int(id))

    return app


def create_database(app):
    # checks if the database exists
    if not path.exists('website/' + DB_NAME):
        db.create_all(app = app)
        print('Created Database!')