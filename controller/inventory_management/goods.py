"""
库存管理  get
"""
import time
import logging

from flask import request, g
from sqlalchemy import or_

import enums
from . import goods_bp, goods_category_bp
from libs.db import Db
from model.goods import Goods, GoodsCategory
from model.record import Record
from tools.render import render_success, render_failed, Pagination
from tools.bind import bind_json, to_json, bind_param
from params.goods import GoodsSaveParams, GoodsParams


@goods_bp.route("/api/goods", methods=["GET", "POST"])
def goods_view():
    if request.method == "GET":
        return get_goods()
    else:
        return create_goods()


def get_goods():
    db = Db()
    param = GoodsParams()
    pagination = Pagination()
    if err := param.check_param():
        return render_failed(msg=err)
    query = db.query(Goods, GoodsCategory).select_from(Goods)
    if param.category_id:
        query = query.filter(GoodsCategory.id == param.category_id)
    if param.keyword:
        keyword = f"%{param.keyword}%"
        query = query.filter(
            or_(Goods.name.like(keyword), Goods.producer.like(keyword), Goods.number.like(keyword)))
    query = query.outerjoin(GoodsCategory, Goods.category_id == GoodsCategory.id)
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
    param = GoodsSaveParams()
    if err := param.check_param():
        return render_failed(msg=err)
    user = g.get(enums.current_user)
    setattr(param, "user_id", user.get("id"))
    # 判断 goods_category表中的id 与接收的id是否一致
    res = db.query(GoodsCategory).filter(GoodsCategory.id == param.category_id).first()
    if not res:
        return render_failed(msg=enums.error_id)
    db.create_one(model=Goods, insert_map=param)
    return render_success()


@goods_bp.route("/api/goods/<goods_id>", methods=["PUT", "DELETE"])
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
    db.session.query(Record).filter(Record.goods_id == goods_id).delete()
    db.delete_one(Goods, goods_id)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()


# 改
def edit_goods(goods_id):
    param = GoodsSaveParams()
    if err := param.check_param():
        return render_failed(msg=err)
    db = Db()
    db.update_one(Goods, goods_id, param)
    return render_success()
