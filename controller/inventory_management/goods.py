"""
库存管理  get
"""
import time
import logging

from flask import request, g

import enums
from . import goods_bp, goods_category_bp
from libs.db import Db
from model.goods import Goods, GoodsCategory
from tools.render import  render_success, render_failed, Pagination
from tools.bind import bind_json, to_json
from params.goods import GoodsParams


@goods_bp.route("/api/goods", methods=["GET", "POST"])
def goods_view():
    if request.method == "GET":
        return get_goods()
    else:
        return create_goods()


def get_goods():
    db = Db()
    pagination = Pagination()
    query = db.query(Goods, GoodsCategory).select_from(Goods).outerjoin(GoodsCategory,
                                                                        Goods.category_id == GoodsCategory.id)
    pagination.total = query.count()
    res = query.order_by(pagination.order_by).offset(pagination.offset).limit(pagination.page_size).all()
    data = {
        "list": [dict(to_json(i), **to_json(n, needList=["type"])) for i, n in res],
        "pagination": pagination.to_dict()
    }
    return render_success(data)



# 增
def create_goods():
    db = Db()
    params = GoodsParams()
    if err := bind_json(params):
        return render_failed(msg=err)
    user = g.get(enums.current_user)
    setattr(params, "user_id", user.get("id"))
    if err := params.required(required_list=["name", "producer", "number", "category_id",
                                             "expired_time", "specification", "unit"]):
        return render_failed(getattr(params, "json"), err)
    # 判断 goods_category表中的id 与接收的id是否一致
    category_id_res = db.query(GoodsCategory).filter(GoodsCategory.id == params.category_id).first()
    if not category_id_res:
        return render_failed("", enums.error_id)
    db.create_one(model=Goods, insert_map=params)
    return render_success()

@goods_category_bp.route("/api/goods/<goods_id>", methods=["PUT", "DELETE"])
def goods_id_view(goods_id):
    if not goods_id:
        return render_failed(msg=enums.error_id)
    goods_id = int(goods_id)
    if request.method == "PUT":
        return edit_goods(goods_id)
    elif request.method == "DELETE":
        return delete_goods(goods_id)
    else:
        return render_failed(msg="nonsupport method", status_code=enums.NonsupportMethod)


# 删
def delete_goods(goods_id):
    db = Db()
    db.delete_one(Goods, goods_id)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()


# 改
def edit_goods(goods_id):
    params = GoodsParams()
    if err := bind_json(params):
        return render_failed(msg=err)
    if err := params.required(required_list=["name", "producer", "number", "category_id",
                                             "expired_time", "specification", "unit"]):
        return render_failed(getattr(params, "json"), err)
    db = Db()
    db.update_one(Goods, goods_id, params)
    return render_success()

# 查
