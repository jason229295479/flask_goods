from . import Base
from enums import lost_param_err


class GoodsCategorySaveParam(Base):
    type = ""

    def _required_verify(self):
        if not self.type:
            return lost_param_err
