import peewee_async
from peewee import *
from conf.op_conf import get_conf

db = peewee_async.PooledMySQLDatabase(
    database=get_conf()['db'],
    user=get_conf()['username'],
    password=get_conf()['password'],
    host=get_conf()['host'],
    port=get_conf()['port']
)

objs = peewee_async.Manager(db)
db.set_allow_sync(True)
# db.set_allow_sync(False)


class BaseModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = db.atomic_async           # 将事务改成atomic_async
        self.objs = peewee_async.Manager(db)   # 添加一个Manager类
    add_time = DateTimeField(null=True, verbose_name="添加时间")

    class Meta:
        database = db


class AccountModel(BaseModel):
    account_id = IntegerField(verbose_name='账号', unique=True)
    username = CharField(max_length=20)
    password = CharField(max_length=30)
    money = IntegerField()
    status = SmallIntegerField()

    class Meta:
        db_table = 'account'


def create_table():
    db.create_tables([AccountModel])


if __name__ == '__main__':
    create_table()