import threading
import logging

from . import DBSession
import enums
from tools.render import Pagination


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

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

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
            self.err = enums.db_error
            return

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

    def query_all(self, model, **kwargs):
        pagination = Pagination()
        query = self.session.query(model).filter_by(**kwargs)
        pagination.total = query.count()
        res = query.order_by(pagination.order_by).offset(pagination.offset).limit(pagination.page_size).all()
        return res, pagination

    def create_one(self, model, insert_map):
        def _create_one():
            self.result = model()
            for key, value in insert_map.json.items():
                if hasattr(self.result, key):
                    setattr(self.result, key, value)
            self.session.add(self.result)

        return self.scope_session(_create_one)

    def __del__(self):
        self.session.close()
