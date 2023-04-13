from flask import Blueprint, render_template

index = Blueprint('/', __name__)


from .registration import registration as registration_blueprint
index.register_blueprint(registration_blueprint)


from .auth import auth as auth_blueprint
index.register_blueprint(auth_blueprint)


from .settings import settings as settings_blueprint
index.register_blueprint(settings_blueprint)


@index.route('/')
def index_page():
    return render_template('index.html')

