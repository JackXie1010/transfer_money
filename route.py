# coding: utf8
from tornado import web
from view import v_index

url_route = [
    (web.url('/*', v_index.head)),
    (web.url('/addAccount', v_index.addAccount)),  # 添加账户接口
    (web.url('/getAccount', v_index.getAccount)),  # 查询账户信息接口
    (web.url('/queryAccounts', v_index.queryAccounts)),  # 查询所有账户接口
    (web.url('/deleteAccount', v_index.deleteAccount)),  # 删除账户接口
    (web.url('/getOrAddMoney', v_index.getOrAddMoney)),  # 存钱或取钱接口，money参数为负数是取钱
    (web.url('/transMoney', v_index.transMoney)),        # 转账接口
]