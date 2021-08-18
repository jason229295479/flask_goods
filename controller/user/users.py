from flask import request, current_app
from sqlalchemy import desc
from . import users_bp
import enums
from tools.render import render_failed, render_success, get_page
from tools import code
from libs import ts, db
from model.user import User


@users_bp.route("/api/users", methods=["GET"])
def users_view():
    if request.method == "GET":
        return get_users()
    else:
        return get_users()


def get_users():
    page, page_size, offset, sort, order = get_page()
    if sort:
        order = desc(order)
    query = db.query(User)
    res = query.order_by(order).offset(offset).limit(page_size).all()
    data = {
        "list": [{
            "id": i.id, "user_name": i.user_name, "mobile": i.mobile,
            "created_time": i.created_time, "updated_time": i.created_time,
        } for i in res],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "order": order,
            "sort": sort,
            "total": query.count()
        }
    }
    return render_success(data)