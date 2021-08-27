from enums import lost_param_err


class Base:
    def required(self, required_list: list = None):
        if required_list:
            if not all([getattr(self, i) for i in required_list]):
                return lost_param_err
