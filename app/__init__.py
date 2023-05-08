import hypercorn.asyncio
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_login import LoginManager
from hypercorn import Config

from .blueprints import BlueprintsRegistrator
from .models.admin import Admin


admin = Admin(id=1, login='', password='')


class FlaskApplication:

    def __init__(self, application_secret):
        self.__app = Flask(__name__)
        self.__app.secret_key = application_secret

        self.__register_blueprints()
        self.__login_manager_register()

        self.__admin = admin

    def __configurate(self):
        pass

    def __register_blueprints(self):
        BlueprintsRegistrator(self.__app)

    def __login_manager_register(self):
        login_manager = LoginManager(self.__app)

        login_manager.init_app(self.__app)

        @login_manager.user_loader
        def load_user(user_id):
            return self.__admin if user_id else None

    def run(self):
        self.__app.run()

    async def hypercon(self):
        asgi_app = WsgiToAsgi(self.__app)

        config = Config()
        port = 5000
        config.bind = [f"0.0.0.0:{port}"]
        await hypercorn.asyncio.serve(asgi_app, Config())
