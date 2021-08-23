import time
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from tools.code import generate_md5
from manage import config

meta = MetaData()

user = Table(
    "user", meta,
    Column('id', Integer, primary_key=True),
    Column('user_name', String(40)),
    Column('mobile', String(40)),
    Column('password', String(40)),
    Column('created_time', Integer),
    Column('updated_time', Integer),
    Column('last_login_time', Integer),
)

goods_category = Table(
    "goods_category", meta,
    Column('id', Integer, primary_key=True),
    Column('type', String(40)),
)

goods = Table(
    "goods", meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('producer', String(40)),
    Column('number', String(40)),
    Column('expired_time', Integer),
    Column('specification', String(40)),
    Column('unit', String(40)),
    Column('inventory_count', Integer),
)

goods_record = Table(
    "goods_record", meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('inventory_count', Integer),
    Column('goods_id', Integer, ForeignKey('goods.id')),
    Column('state', String(40)),
    Column('operation_time', Integer),
    Column('operator_id', Integer, ForeignKey('user.id')),
    Column('remark', String(40)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user.create()
    res = user.insert().values(user_name="admin", mobile=config.get("DEFAULT_MOBILE"),
                               password=generate_md5(config.get("SALT") + config.get("DEFAULT_PASSWORD")),
                               created_time=int(time.time()))
    migrate_engine.execute(res)
    goods_category.create()
    goods.create()
    goods_record.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    goods_category.drop()
    user.drop()
    goods_record.drop()
    goods.drop()
