from control.base import BaseControl
from playhouse.shortcuts import model_to_dict


class PublicControl(BaseControl):
    async def table_add(self, model, table, arg):
        try:
            obj = await model.objs.create(table, **arg)
        except:
            print('excep: table_add error')
            obj = 0
        return obj

    async def table_delete(self, model, sql):
        try:
            num = await model.objs.execute(sql)
        except:
            print('excep: table_delete error')
            num = 0
        return num

    async def table_update(self, model, sql):
        # num = await model.objs.execute(sql)
        try:  # success: num=1
            num = await model.objs.execute(sql)
        except:
            print('excep: table_update error')
            num = 0
        return num

    async def table_get(self, model, sql):
        try:
            obj = await model.objs.get(sql)
            obj = model_to_dict(obj)
        except:
            print('excep: table_get error')
            obj = 0
        return obj

    async def table_find(self, model, sql):
        try:
            data = await model.objs.execute(sql)
            lst = []
            for v in data:
                v = model_to_dict(v)
                lst.append(v)
        except:
            print('excep: table_find error')
            lst = []
        return lst