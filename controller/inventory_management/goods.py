"""
库存管理 post
"""
from flask import request

import enums
from libs import db
from model.user import GoodsCategory, Goods
from tools.render import render_success, render_failed
from . import goods_bp, goods_category_bp


# 添加商品类别
@goods_category_bp.route("/api/goods_category_bp", methods=["POST"])
def goods_category_view():
    type = request.json.get("type")
    category = GoodsCategory(type=type)
    db.add(category)
    db.commit()
    return render_success()


# 商品视图
@goods_bp.route("/api/goods", methods=["POST"])
def goods_view():
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
