"""
库存管理  get
"""
import time

from flask import request, session
from sqlalchemy import desc
import logging

from libs import db
from model.goods import Goods, GoodsCategory
from tools.render import get_page, render_success, render_failed
from . import goods_bp, goods_category_bp
import enums


@goods_category_bp.route("/api/goods_category", methods=["GET"])
def goods_category_view():
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


# 增
@goods_category_bp.route("/api/goods_category", methods=["POST"])
def create_goods_category():
    goods_type = request.json.get("type")
    category = GoodsCategory(type=goods_type)
    db.add(category)
    db.commit()
    return render_success()


# 改
@goods_category_bp.route("/api/goods_category", methods=["PUT"])
def edit_goods_category():
    # 前端获取
    goods_category_id = request.json.get("id")
    goods_type = request.json.get("type")
    if not all([goods_type, goods_category_id]):
        return render_failed("", enums.param_err)
    goods_category_id = int(goods_category_id)
    # 数据库查询
    goods_category = db.query(GoodsCategory).filter(GoodsCategory.id == goods_category_id).first()
    if not goods_category:
        return render_failed("", enums.error_id)
    goods_category.type = goods_type
    # 更新
    db.commit()
    return render_success()


# 删
@goods_category_bp.route("/api/goods_category", methods=["DELETE"])
def delete_goods_category():
    # 前端获取
    goods_category_id = request.json.get("id")

    if not all([goods_category_id]):
        return render_failed("", enums.param_err)
    goods_category_id = int(goods_category_id)
    # 数据库查询
    category_id = db.query(GoodsCategory).filter(GoodsCategory.id == goods_category_id).first()
    if not category_id:
        return render_failed("", enums.error_id)
    # 删除
    Goods.category = " "
    db.delete(category_id)
    # 更新
    db.commit()
    return render_success()


@goods_bp.route("/api/goods", methods=["GET"])
def goods_view():
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


# 增
@goods_bp.route("/api/goods", methods=["POST"])
def create_goods():
    name = request.json.get("name")
    producer = request.json.get("producer")
    number = request.json.get("number")
    category_id = request.json.get("category_id")
    expired_time = request.json.get("expired_time")
    specification = request.json.get("specification")
    unit = request.json.get("unit")
    inventory_count = request.json.get("inventory_count")
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
        expired_time = int(time.mktime(time.strptime(expired_time, "%Y-%m-%d")))
        # expired_time = int(expired_time)
        inventory_count = int(inventory_count)
    except Exception as e:
        logging.info(f"try to covert str to int failed:{str(e)}")
        return render_failed(" ", str(e))
    goods = Goods(name=name, producer=producer, number=number,
                  category=category_id, expired_time=expired_time, specification=specification,
                  unit=unit, inventory_count=inventory_count, )
    # 更新数据库
    db.add(goods)
    db.session.commit()
    return render_success()


# 删
@goods_bp.route("/api/goods", methods=["DELETE"])
def delete_goods():
    goods_id = request.json.get("id")

    if not all([goods_id]):
        return render_failed("", enums.param_err)
    goods_id = int(goods_id)

    # 数据库查询
    id_res = db.query(Goods).filter(Goods.id == goods_id).first()
    if not id_res:
        return render_failed("", enums.error_id)
    # 删
    db.delete(id_res)
    db.commit()

    # 更新
    return render_success()


# 改
@goods_bp.route("/api/goods", methods=["PUT"])
def edit_goods():
    # 前端获取
    goods_id = request.json.get("id")
    name = request.json.get("name")
    producer = request.json.get("producer")
    number = request.json.get("number")
    category_id = request.json.get("category_id")
    expired_time = request.json.get("expired_time")
    specification = request.json.get("specification")
    unit = request.json.get("unit")
    inventory_count = request.json.get("inventory_count")

    if not all([goods_id, name, producer, number, expired_time, specification, unit, inventory_count]):
        return render_failed("", enums.param_err)
    try:
        goods_id = int(goods_id)
        category_id = int(category_id)
        expired_time = int(time.mktime(time.strptime(expired_time, "%Y-%m-%d")))
        inventory_count = int(inventory_count)
    except Exception as e:
        logging.info(f"try to covert str to int failed:{str(e)}")
        return render_failed(" ", str(e))

    # 数据库查询
    id_res = db.query(Goods).filter(Goods.id == goods_id).first()
    if not id_res:
        return render_failed("", enums.error_id)

    id_res.id = goods_id
    id_res.name = name
    id_res.producer = producer
    id_res.number = number
    id_res.category_id = category_id
    id_res.expired_time = expired_time
    id_res.specification = specification
    id_res.unit = unit
    id_res.inventory_count = inventory_count
    # 更新
    db.commit()
    return render_success()

# 查
