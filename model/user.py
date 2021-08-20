import time
from sqlalchemy import Column, String, INT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = "user"

    # 表的结构:
    id = Column(INT(), primary_key=True)
    user_name = Column(String(), )
    mobile = Column(String(), )
    password = Column(String(), )
    last_login_time = Column(INT(), default=0)
    created_time = Column(INT(), default=int(time.time()))
    updated_time = Column(INT(), default=int(time.time()), onupdate=int(time.time()))


class GoodsCategory(Base):
    # 表的名字:
    __tablename__ = "goods_category"

    id = Column(INT(), primary_key=True)
    type = Column(String(), )  # 商品类别


# 定义Goods对象:
class Goods(Base):
    # 表的名字:
    __tablename__ = "goods"
    # 表的结构:
    id = Column(INT(), primary_key=True)  # id号
    name = Column(String(), )  # 商品名称
    producer = Column(String(), )  # 生产商
    number = Column(String(), )  # 药械准字号
    category = Column(INT(), ForeignKey('goods_category.id'))  # 物品类别
    expiring = Column(INT(), default=int(time.time()))  # 有效日期
    specification = Column(String(), )  # 规格信息
    unit = Column(String(), )  # 单位
    inventory_count = Column(INT(), )  # 库存数量


class Record(Base):
    # 表的名字:
    __tablename__ = "goods_record"
    id = Column(INT(), primary_key=True)  # id号
    name = Column(String(), )  # 商品名称
    inventory_count = Column(INT(), )  # 出入库数量
    category = Column(INT(), ForeignKey('goods_category.id'))  # 物品类别
    state = Column(String(), )  # 操作状态 ，出库、入库
    operation_time = Column(INT(), default=int(time.time()))  # 操作时间
    operator = Column(String(), ForeignKey('user.id'))  # 操作人
    remark = Column(String(), )  # 备注
