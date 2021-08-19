from flask import Blueprint

from middleware.jwt_handel import jwt_request

record_bps = Blueprint('records', __name__)
record_bps.before_request(jwt_request)
