# 出入库视图

from flask import request

import enums

from libs import db
from model.user import Record
from tools.render import render_failed, render_success
from . import record_bps


@record_bps.route("/api/records", methods=["POST"])
def record_view():
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
                    state=state, operation_time=operation_time, operator=operator,
                    remark=remark)
    # 更新数据库
    db.add(record)
    db.commit()
    return render_success()
