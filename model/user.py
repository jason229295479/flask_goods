import time

from sqlalchemy import Column, String, INT, ForeignKey

from .base import Base


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
    name = Column(String(), )  # 商品类别


