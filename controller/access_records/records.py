# 出入库视图
import time

from flask import request, g

from libs.db import Db
from model.record import Record
from model.goods import Goods
from model.user import User
from tools.render import render_failed, render_success, to_json, Pagination
from tools.bind import bind_json, bind_param
from . import record_bps
import enums
from params.record import RecordSaveParam, RecordParam


@record_bps.route("/api/records", methods=["GET", "POST"])
def record_view():
    if request.method == "GET":
        return get_record()
    elif request.method == "POST":
        return create_record()
    else:
        return render_failed(msg="nonsupport method", status_code=enums.NonsupportMethod)


def get_record():
    db = Db()
    param = RecordParam()
    pagination = Pagination()
    if err := bind_param(param):
        return render_failed(msg=err)
    query = db.query(Record, Goods, User).select_from(Record)
    if param.goods_id:
        goods = db.query(Goods).filter(Goods.id == param.goods_id).first()
        if not goods:
            return render_failed("", enums.error_id)
        query = query.filter(Goods.id == param.goods_id)
    if param.state:
        query = query.filter(Record.state == param.state)
    query = query.outerjoin(Goods, Goods.id == Record.goods_id). \
        outerjoin(User, User.id == Record.operator_id)
    pagination.total = query.count()
    res = query.order_by(pagination.order_by).offset(pagination.offset).limit(pagination.page_size).all()
    data = {
        "list": [dict(to_json(record, ignoreList=["operator_id", "goods_id"]), **to_json(goods, needList=["name"]),
                      **to_json(user, needList=["user_name"])) for
                 record, goods, user in res],
        "pagination": pagination.to_dict()
    }
    return render_success(data)


def create_record():
    param = RecordSaveParam()
    if err := param.check_param():
        return render_failed(msg=err)
    db = Db()
    goods = db.query(Goods).filter(Goods.id == param.goods_id).first()
    if not goods:
        return render_failed("", enums.error_id)
    user = g.get(enums.current_user)
    setattr(param, "operator_id", user.get("id"))
    setattr(param, "operation_time", int(time.time()))
    if param.state < 0:
        goods.inventory_count -= param.inventory_count
        if goods.inventory_count < 0:
            return render_failed(msg=enums.inventory_count_lack)
    else:
        goods.inventory_count += param.inventory_count
    db.create_one(Record, param)
    if db.err:
        return render_failed(msg=db.err)
    return render_success()
