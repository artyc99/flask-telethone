import json

from flask import Blueprint

from .response import response200

admin = Blueprint('/admin', __name__)


@admin.route('/test', methods=['POST', 'GET'])
def test():
    return response200(json.dumps({'test': 'test', 'test2':'test2'}), mimetype='application/json')
