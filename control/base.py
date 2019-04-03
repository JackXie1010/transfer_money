from models import *


class BaseControl(object):
    def __init__(self, *args, **kwargs):
        super(BaseControl, self).__init__(*args, **kwargs)
        self.account_model = AccountModel()

    def res_ok(self, code=200, data=1, msg='请求成功！'):
        return dict(code=code, data=data, msg=msg)

    def res_err(self, code=204, data=0, msg='请求失败！'):
        return dict(code=code, data=data, msg=msg)
