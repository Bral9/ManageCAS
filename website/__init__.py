from flask import Flask
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from .database import db      # ✅ use the shared db
import os

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fndbnfjdhfdnjfd')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # init extensions
    CKEditor(app)
    db.init_app(app)

    # blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        from .models import Admin, Teacher, Student
        # Prefer Admin → Teacher → Student
        return (Admin.query.filter_by(email=email).first()
                or Teacher.query.filter_by(email=email).first()
                or Student.query.filter_by(email=email).first())

    # create tables once the app & models are registered
    with app.app_context():
        from . import models   # ensures models use the SAME db
        db.create_all()
        print("DB in use:", db.engine.url)

    return app