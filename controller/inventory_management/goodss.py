"""
库存管理  get
"""

from flask import request
from sqlalchemy import desc

from libs import db
from model.user import Goods, GoodsCategory
from tools.render import get_page, render_success
from . import goods_bp, goods_category_bp


@goods_category_bp.route("/api/goods_category", methods=["GET"])
def goods_category_view():
    if request.method == "GET":
        return get_goods_category()
    else:
        return get_goods_category()


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


@goods_bp.route("/api/goods", methods=["GET"])
def goods_view():
    if request.method == "GET":
        return get_goods()
    else:
        return get_goods()


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
