from flask import Blueprint

from middleware.jwt_handel import jwt_request

goods_bp = Blueprint('goods', __name__)
goods_category_bp = Blueprint('goods_category', __name__)


goods_bp.before_request(jwt_request)
goods_category_bp.before_request(jwt_request)

