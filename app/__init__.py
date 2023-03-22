from flask import Flask


from .blueprints import BlueprintsRegistrator


class FlaskApplication:

    def __init__(self):
        self.__flaskApp = Flask(__name__)

        self.__register_blueprints()

    def __configurate(self):
        pass

    def __register_blueprints(self):
        BlueprintsRegistrator(self.__flaskApp)

    def run(self):
        self.__flaskApp.run()
