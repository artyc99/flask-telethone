from flask import Blueprint

api = Blueprint('/api', __name__)

from .admin import admin as admin_bluerints
api.register_blueprint(admin_bluerints)

