from datetime import date, datetime
from tornado import web
from conf import jwt_token
from control.c_index import IndexControl
import json


class DateEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


class BaseHandler(web.RequestHandler):
    # 设置请求头
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header(
            'Access-Control-Allow-Headers',
            'Content-Type, token, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods'
        )
        self.ctrl_index = IndexControl()

    def options(self, *args, **kwargs):
        pass

    def to_json(self, arg):
        try:
            res = json.dumps(arg, cls=DateEncoder)
        except:
            res = arg
        return res

    def to_dict(self, arg):
        try:
            res = json.loads(arg)
        except:
            res = arg
        return res

    def finish_ok(self, data=1, code=200, msg='请求成功'):
        obj = dict(code=code, data=data, msg=msg)
        return self.write(self.to_json(obj))

    def finish_err(self, data=1, code=204, msg='请求失败'):
        obj = dict(code=code, data=data, msg=msg)
        return self.write(self.to_json(obj))

    def validate_arg(self, right_arg, arg, is_valid_tonken=0):
        def w(func):
            def inner():
                if type(right_arg) != list and type(arg) != dict:
                    diff = 1
                else:
                    diff = list(set(right_arg).difference(set(arg)))
                if diff:
                    msg = '校验的参数格式错误' if 1 == diff else '缺少的参数有：%s' % diff
                    ret = {'msg': msg, 'code': 604, 'data': ''}
                else:
                    try:
                        if not is_valid_tonken:
                            data = func()
                            ret = {'msg': '', 'code': 200, 'data': data}
                        else:
                            result = jwt_token.validate_token(arg['token'])  # result = {res:0/1, msg:payload}
                            if result['res']:
                                data = func()
                                ret = {'msg': '', 'code': 200, 'data': data}
                            else:
                                ret = {'msg': '用户信息有误，请重新登录', 'code': 204, 'data': 1}
                    except:
                        ret = {'msg': '系统异常', 'code': 999, 'data': ''}
                return ret
            return inner
        return w