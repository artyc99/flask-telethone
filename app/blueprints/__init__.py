

class BlueprintsRegistrator:
    def __init__(self, application: Flask):
        from .rsaApi import rsaApi as rsaApiBlueprint
        application.register_blueprint(rsaApiBlueprint)
