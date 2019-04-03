# 银行转账服务
主要功能：事务实现转账功能
主要知识：tornado， pipenv环境管理，peewee, peewee_async, 异步非组赛，jwt
 接口：
1./addAccount    # 添加账户接口
2./getAccount    # 查询账户信息接口
3./queryAccounts # 查询所有账户接口
4./deleteAccount # 删除账户接口
5./getOrAddMoney # 存钱或取钱接口，money参数为负数是取钱
6./transMoney    # 转账接口

启动：
python server.py --dev=False --port=8888 --debug=False
dev参数主要用来决定是否是读取开发环境的配置还是生产环境的配置
