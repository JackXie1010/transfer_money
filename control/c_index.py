from control.base import BaseControl
from control.c_public import PublicControl
from models import AccountModel
from datetime import datetime

a, b, c, d = AccountModel.add_time, AccountModel.money, AccountModel.username, AccountModel.account_id

class IndexControl(BaseControl):
    async def addAccount(self, arg):
        if 'money' not in arg: arg['money'] = 0
        arg['add_time'], arg['status'] = datetime.now(), 1
        obj = await PublicControl.table_add(self, self.account_model, AccountModel, arg)
        res = self.res_ok(msg='添加成功！') if obj else self.res_err(msg='添加失败！')
        return res

    async def getAccount(self, arg):
        sql = AccountModel.select(a, b, c, d).where(AccountModel.account_id==arg['account_id'])
        obj = await PublicControl.table_get(self, self.account_model, sql)
        return self.res_ok(data=obj)

    async def queryAccounts(self, arg):
        start = (int(arg['curr_page']) - 1) * int(arg['page_num'])
        sql = AccountModel.select(a, b, c, d ).where(AccountModel.status==1).limit(arg['page_num']).offset(start)
        lst = await PublicControl.table_find(self, self.account_model, sql)
        return self.res_ok(data=lst)

    async def deleteAccount(self, arg):
        sql = AccountModel.delete().where(AccountModel.account_id == arg['account_id'])
        num = await PublicControl.table_delete(self, self.account_model, sql)
        res = self.res_ok(msg='删除成功！') if num else self.res_err(msg='删除失败！')
        return res

    async def getRemindMoney(self, account_id):
        sql = AccountModel.select(AccountModel.money).where(AccountModel.account_id == account_id)
        obj = await PublicControl.table_get(self, self.account_model, sql)
        return obj

    async def getOrAddMoney(self, arg):
        if arg['money'] < 0:  # arg['money'] < 0 为取钱，取钱时要判断约是否大于要取出的金额
            print('取钱')
            obj = await self.getRemindMoney(arg['account_id'])
            if (obj['money'] + arg['money']) < 0:
                return self.res_err(msg='您的余额不足！')
        sql = AccountModel.update(money=AccountModel.money + arg['money']).where(AccountModel.account_id == arg['account_id'])
        num = await PublicControl.table_update(self, self.account_model, sql)
        res = self.res_ok() if num else self.res_err()
        return res

    async def transMoney(self, arg):
        try:
            async with self.account_model.trans():  # 一个账户转出钱，一个账户转入钱，同时成功或回滚
                obj = await self.getRemindMoney(arg['out_account_id'])
                if obj['money'] < arg['money']: return self.res_err(msg='余额不足')
                sql = AccountModel.update(money=AccountModel.money - arg['money']).where(AccountModel.account_id == arg['out_account_id'])
                num = await PublicControl.table_update(self, self.account_model, sql)
                if not num: raise RuntimeError('转钱失败！')
                sql = AccountModel.update(money=AccountModel.money + arg['money']).where(AccountModel.account_id == arg['in_account_id'])
                num = await PublicControl.table_update(self, self.account_model, sql)
                if not num: raise RuntimeError('收钱失败！')
            res = self.res_ok()
        except:
            res = self.res_err()
        return res

