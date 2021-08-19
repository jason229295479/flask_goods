from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

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
    Column('category', Integer, ForeignKey('goods_category.id')),
    Column('expiring', Integer),
    Column('specification', String(40)),
    Column('unit', String(40)),
    Column('inventory_count', String(40)),
)

goods_record = Table(
    "goods_record", meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('inventory_count', Integer),
    Column('category', Integer, ForeignKey('goods_category.id')),
    Column('state', String(40)),
    Column('operation_time', Integer),
    Column('operator', Integer, ForeignKey('user.id')),
    Column('remark', String(40)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    user.create()
    goods_category.create()
    goods.create()
    goods_record.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    user.drop()
    goods_category.drop()
    goods.drop()
    goods_record.drop()
