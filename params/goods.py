from . import Base


class GoodsSaveParams(Base):
    name = ""
    producer = ""
    number = ""
    category_id = 0
    expired_time = 0
    specification = ""
    unit = ""


class GoodsParams(Base):
    category_id = 0
    keyword = ""
