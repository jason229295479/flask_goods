# 出入库视图
import logging
import time

from flask import request
from sqlalchemy import desc

import enums
from libs import db
from model.record import Record
from tools.render import get_page, render_success, render_failed
from . import record_bps


@record_bps.route("/api/records", methods=["GET"])
def record_view():
    return create_record()


def get_record():
    page, page_size, offset, sort, order = get_page()
    if sort:
        order = desc(order)
    query = db.query(Record)
    res = query.order_by(order).offset(offset).limit(page_size).all()
    data = {
        "list": [{
            "id": i.id,
            "type": i.name,
            "inventory_count": i.inventory_count,
            "category": i.category,
            "state": i.state,
            "operation_time": i.operation_time,
            "operatoroperator": i.operator,
            "remarkremark": i.remark,

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


@record_bps.route("/api/records", methods=["POST"])
def create_record():
    name = request.json.get("name")
    inventory_count = request.json.get("inventory_count")
    goods_id = request.json.get("goods.id")
    state = request.json.get("state")
    operation_time = request.json.get("operation_time")
    operator_id = request.json.get("user.id")
    remark = request.json.get("remark")
    # 数据不能为空
    if not all([name, inventory_count, goods_id,
                state, operation_time, operator_id, remark]):
        return render_failed(" ", enums.param_err)
    try:
        goods_id = int(goods_id)
        inventory_count = int(inventory_count)
        state = int(state)
        operation_time = int(time.mktime(time.strptime(operation_time, "%Y-%m-%d")))
    #    expired_time = datetime.strptime(expired_time, "%Y-%m-%d")
        operator_id = int(operator_id)
    except Exception as e:
        logging.info(f"try to covert str to int failed:{str(e)}")
        return render_failed(" ", str(e))
    record = Record(name=name, inventory_count=inventory_count, category=goods_id,
                    state=state, operation_time=operation_time, operator_id=operator_id,
                    remark=remark)
    # 更新数据库
    db.add(record)
    db.commit()
    return render_success()
