import time

from sqlalchemy import Column, String, INT, ForeignKey

from .base import Base


class Record(Base):
    # 表的名字:
    __tablename__ = "goods_record"
    id = Column(INT(), primary_key=True)  # id号
    name = Column(String(), )  # 商品名称
    inventory_count = Column(INT(), )  # 出入库数量
    goods_id = Column(INT(), ForeignKey('goods.id'))  # 物品
    state = Column(INT(), default=1)  # 操作状态 ，-1出库、1入库 默认入库
    operation_time = Column(INT(), default=int(time.time()))  # 操作时间
    operator_id = Column(INT(), ForeignKey('user.id'))  # 操作人
    remark = Column(String(), )  # 备注