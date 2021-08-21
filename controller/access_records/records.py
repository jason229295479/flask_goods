# 出入库视图

from flask import request
from sqlalchemy import desc

import enums
from libs import db
from model.record import Record
from tools.render import get_page, render_success, render_failed
from . import record_bps


@record_bps.route("/api/records", methods=["GET,POST"])
def record_view():
    if request.method == "GET":
        return get_record()
    else:
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


def create_record():
    name = request.json.get("name")
    inventory_count = request.json.get("inventory_count")
    category = request.json.get("goods_category.id")
    state = request.json.get("state")
    operation_time = request.json.get("operation_time")
    operator = request.json.get("goods_id")
    remark = request.json.get("remark")
    # 数据不能为空
    if not all([name, inventory_count, category,
                state, operation_time, operator, remark]):
        return render_failed(" ", enums.param_err)
    record = Record(name=name, inventory_count=inventory_count, category=category,
                    state=state, operation_time=operation_time, operator_id=operator,
                    remark=remark)
    # 更新数据库
    db.add(record)
    db.commit()
    return render_success()
