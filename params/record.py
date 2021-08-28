from . import Base
import enums


class RecordSaveParam(Base):
    inventory_count = 0
    goods_id = 0
    state = 0
    remark = ""

    def verify(self):
        if self.inventory_count < 0:
            return enums.error_inventory_count
        if self.state not in [1, 0, -1]:
            return enums.error_state
        if self.goods_id <= 0:
            return enums.error_id


class RecordParam(Base):
    state = 0
    goods_id = 0
