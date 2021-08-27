# 出入库视图


from flask import request

import enums
from libs import DBSession
from libs.db import Db
from model.goods import Goods

from model.record import Record
from tools.bind import bind_json
from tools.render import get_page, render_success, render_failed
from . import record_bps
from params.records import RecordsParams


@record_bps.route("/api/records", methods=["GET"])
def record_view():
    if request.method == "GET":
        return get_record()


def get_record():
    db = DBSession()
    page, page_size, offset, sort, order = get_page()
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


# 增
@record_bps.route("/api/records", methods=["POST"])
def create_record():
    # 先更新库存
    pass


