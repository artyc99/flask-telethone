from flask import Response

CHARSET = 'utf-8'
DEFAULT_MIMETYPE = 'application/json'


def response200(data=None, charset: str = CHARSET, mimetype: str = DEFAULT_MIMETYPE) -> Response:
    if data is None:
        data = {}

    return Response(headers={'Access-Control-Allow-Origin': '*'}, response=data, mimetype=mimetype)