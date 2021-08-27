from . import users_bp
from tools.render import render_success
from tools.bind import to_json
from model.user import User
from libs.db import Db


@users_bp.route("/api/users", methods=["GET"])
def users_view():
    return get_users()


def get_users():
    db = Db()
    res, pagination = db.query_all(User)
    data = {
        "list": [to_json(i, ignoreList=["password"]) for i in res],
        "pagination": pagination.to_dict()
    }
    return render_success(data)
