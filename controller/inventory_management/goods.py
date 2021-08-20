"""
库存管理  get
"""

from flask import request
from sqlalchemy import desc

from libs import db
from model.user import Goods, GoodsCategory
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
    category = request.json.get("goods_category.id")
    expiring = request.json.get("expiring")
    specification = request.json.get("specification")
    unit = request.json.get("unit")
    inventory_count = request.json.get("inventory_count")
    # 数据不能为空
    if not all([name, producer, number, category,
                expiring, specification, unit, inventory_count]):
        return render_failed(" ", enums.param_err)
    goods = Goods(name=name, producer=producer, number=number,
                  category=category, expiring=expiring, specification=specification,
                  unit=unit, inventory_count=inventory_count, )
    # 更新数据库
    db.add(goods)
    db.commit()
    return render_success()
