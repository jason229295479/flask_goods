"""
库存管理  get
"""

from flask import request
from sqlalchemy import desc
import logging

from libs import db
from model.goods import Goods, GoodsCategory
from tools.render import get_page, render_success, render_failed
from . import goods_bp, goods_category_bp
import enums


@goods_category_bp.route("/api/goods_category", methods=["GET,POST"])
def goods_category_view():
    if request.method == "GET":
        return get_goods_category()
    else:
        return create_goods_category()


def get_goods_category():
    page, page_size, offset, sort, order = get_page()
    if sort:
        order = desc(order)
    query = db.query(GoodsCategory)
    res = query.order_by(order).offset(offset).limit(page_size).all()
    data = {
        "list": [{
            "id": i.id,
            "type": i.type,
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


def create_goods_category():
    goods_type = request.json.get("type")
    category = GoodsCategory(type=goods_type)
    db.add(category)
    db.commit()
    return render_success()


@goods_bp.route("/api/goods", methods=["GET,POST"])
def goods_view():
    if request.method == "GET":
        return get_goods()
    else:
        return create_goods()


def get_goods():
    page, page_size, offset, sort, order = get_page()
    if sort:
        order = desc(order)
    query = db.query(Goods)
    res = query.order_by(order).offset(offset).limit(page_size).all()
    data = {
        "list": [{
            "id": i.id,
            "name": i.name,
            "number": i.number,
            "category": i.category,
            "expiring": i.expiring,
            "specification": i.specification,
            "unit": i.unit,
            "inventory_count": i.inventory_count,
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


def create_goods():
    name = request.json.get("name")
    producer = request.json.get("producer")
    number = request.json.get("number")
    category_id = request.json.get("category_id")
    expired_time = request.json.get("expired_time")
    specification = request.json.get("specification")
    unit = request.json.get("unit")
    inventory_count = request.json.get("inventory_count")
    # 数据不能为空
    if not all([name, producer, number, category_id,
                expired_time, specification, unit, inventory_count]):
        return render_failed(" ", enums.param_err)
    try:
        category_id = int(category_id)
        expired_time = int(expired_time)
        inventory_count = int(inventory_count)
    except Exception as e:
        logging.info(f"try to covert str to int failed:{str(e)}")
        return render_failed(" ", str(e))
    goods = Goods(name=name, producer=producer, number=number,
                  category_id=category_id, expired_time=expired_time, specification=specification,
                  unit=unit, inventory_count=inventory_count, )
    # 更新数据库
    db.add(goods)
    db.commit()
    return render_success()
