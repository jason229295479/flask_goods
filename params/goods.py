from . import Base
from enums import lost_param_err


class GoodsSaveParams(Base):
    name = ""
    producer = ""
    number = ""
    category_id = 0
    expired_time = 0
    specification = ""
    unit = ""

    def _required_verify(self):
        if not all([self.name, self.producer, self.number, self.category_id, self.expired_time, self.specification,
                    self.unit]):
            return lost_param_err


class GoodsParams(Base):
    category_id = 0
    keyword = ""
