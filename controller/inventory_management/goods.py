"""
库存管理  get
"""

import logging

from flask import request

import enums
from . import goods_bp
from libs import DBSession
from libs.db import Db
from model.goods import Goods, GoodsCategory
from tools.render import get_page, render_success, render_failed
from tools.bind import bind_json
from params.goods import GoodsParams


@goods_bp.route("/api/goods", methods=["GET", "POST"])
def goods_view():
    if request.method == "GET":
        return get_goods()
    else:
        return create_goods()


def get_goods():
    db = DBSession()
    page, page_size, offset, sort, order = get_page()
    query = db.query(Goods, GoodsCategory).select_from(Goods).outerjoin(GoodsCategory,
                                                                        Goods.category_id == GoodsCategory.id)
    res = query.order_by(order).offset(offset).limit(page_size).all()
    data = {
        "list": [{
            "id": i.id,
            "name": i.name,
            "number": i.number,
            "producer": i.producer,
            "category_id": i.category_id,
            "expired_time": i.expired_time,
            "specification": i.specification,
            "unit": i.unit,
            "type": n.type,
            "inventory_count": i.inventory_count,
            "created_time": i.created_time,
            "updated_time": i.created_time,
        } for i, n in res],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "order": order,
            "sort": sort,
            "total": query.count()
        }
    }
    return render_success(data)


# 增
def create_goods():
    db = DBSession()
    name = request.json.get("name")
    producer = request.json.get("producer")
    number = request.json.get("number")
    category_id = request.json.get("category_id")
    expired_time = request.json.get("expired_time")
    specification = request.json.get("specification")
    unit = request.json.get("unit")
    # 新建商品默认为0 ,出入库操作是添加库存
    inventory_count = 0
    # 判断 goods_category表中的id 与接收的id是否一致
    category_id_res = db.query(GoodsCategory).filter(GoodsCategory.id == category_id).first()
    if not category_id_res:
        return render_failed("", enums.error_id)
    # 数据不能为空
    if not all([name, producer, number, category_id,
                expired_time, specification, unit, inventory_count]):
        return render_failed(" ", enums.param_err)
    try:
        category_id = int(category_id)
        expired_time = int(expired_time)
        # expired_time = int(expired_time)
        inventory_count = int(inventory_count)
    except Exception as e:
        logging.info(f"try to covert str to int failed:{str(e)}")
        return render_failed(" ", str(e))
    goods = Goods(name=name, producer=producer, number=0,
                  category_id=category_id, expired_time=expired_time, specification=specification,
                  unit=unit, inventory_count=inventory_count, )
    # 更新数据库
    db.add(goods)
    db.commit()
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
    db.delete_one(Goods, goods_id)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()


# 改
def edit_goods(goods_id):
    params = GoodsParams()
    if err := bind_json(params):
        return render_failed(msg=err)
    db = Db()
    db.update_one(Goods, goods_id, params)
    return render_success()

# 查
