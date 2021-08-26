import threading
import logging

from . import DBSession
import enums


class Db:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Db, "_instance"):
            with Db._instance_lock:
                if not hasattr(Db, "_instance"):
                    Db._instance = object.__new__(cls)
        return Db._instance

    def __init__(self):
        self.session = DBSession()
        self.err = None
        self.result = None

    def scope_session(self, func):
        try:
            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            inner()
            self.session.commit()
            return
        except Exception as e:
            # if any kind of exception occurs, rollback transaction
            logging.error(e)
            self.session.rollback()
            return str(e)
        finally:
            self.session.close()

    def delete_one(self, model, operate_id):
        def _delete_one():
            # 数据库查询
            self.result = self.session.query(model).filter(model.id == operate_id).first()
            if not self.result:
                self.err = enums.error_id
                return
                # 删除
            self.session.delete(self.result)

        return self.scope_session(_delete_one)

    def update_one(self, model, operate_id, update_map):
        def _update_one():
            self.result = self.session.query(model).filter(model.id == operate_id).first()
            if not self.result:
                self.err = enums.error_id
                return
            for key, value in update_map.json.items():
                if hasattr(self.result, key):
                    setattr(self.result, key, value)
        return self.scope_session(_update_one)
