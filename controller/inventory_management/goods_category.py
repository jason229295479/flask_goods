"""
库存管理  get
"""

from flask import request

from model.goods import GoodsCategory
from tools.render import render_success, render_failed, to_json
from . import goods_category_bp
import enums
from libs.db import Db
from params.goods_category import GoodsCategorySaveParam


@goods_category_bp.route("/api/goods/category", methods=["GET", "POST"])
def goods_category_view():
    if request.method == "GET":
        return get_goods_category()
    elif request.method == "POST":
        return create_goods_category()
    else:
        return render_failed(msg="nonsupport method", status_code=enums.NonsupportMethod)


def get_goods_category():
    db = Db()
    res, pagination = db.query_all(GoodsCategory)
    data = {
        "list": [to_json(i) for i in res],
        "pagination": pagination.to_dict()
    }
    return render_success(data)


# 增
def create_goods_category():
    db = Db()
    param = GoodsCategorySaveParam()
    if err := param.check_param():
        return render_failed(msg=err)
    db.create_one(GoodsCategory, param)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()


@goods_category_bp.route("/api/goods/category/<category_id>", methods=["PUT", "DELETE"])
def goods_category_id_view(category_id):
    if not category_id:
        return render_failed(msg=enums.error_id)
    category_id = int(category_id)
    if request.method == "PUT":
        return edit_goods_category(category_id)
    elif request.method == "DELETE":
        return delete_goods_category(category_id)
    else:
        return render_failed(msg="nonsupport method", status_code=enums.NonsupportMethod)


def edit_goods_category(category_id):
    db = Db()
    param = GoodsCategorySaveParam()
    if err := param.check_param():
        return render_failed(msg=err)
    db.update_one(GoodsCategory, category_id, param)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()


# 删
def delete_goods_category(category_id):
    db = Db()
    db.delete_one(GoodsCategory, category_id)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()
