from flask import Flask


class BlueprintsRegistrator:
    def __init__(self, application: Flask):
        from .api import api as apiBlueprint
        application.register_blueprint(apiBlueprint)

        from .pages import index as pagesBlueprint
        application.register_blueprint(pagesBlueprint)
