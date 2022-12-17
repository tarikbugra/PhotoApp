from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloworld"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)
    admin = Admin(app)

    from .models import Photo, PhotoView, User, UserView
    admin.add_view(UserView(User, db.session))
    admin.add_view(PhotoView(Photo, db.session))

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
