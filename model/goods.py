import time

from sqlalchemy import Column, String, INT, ForeignKey

from .base import Base


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
    # category = Column(INT(), ForeignKey('goods_category.id'))  # 物品类别
    category = Column(INT(), index=True)
    expired_time = Column(INT(), default=int(time.time()))  # 有效日期
    specification = Column(String(), )  # 规格信息
    unit = Column(String(), )  # 单位
    inventory_count = Column(INT(), )  # 库存数量
