from view.base import BaseHandler


class head(BaseHandler):
    async def get(self):
        self.finish_err()

    async def post(self):
        self.finish_err()


class addAccount(BaseHandler):
    async def post(self):
        arg = self.to_dict(self.request.body)

        @self.validate_arg(['account_id', 'username', 'password'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.addAccount(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)


class getAccount(BaseHandler):
    async def post(self):
        arg = self.to_dict(self.request.body)

        @self.validate_arg(['account_id'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.getAccount(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)


class queryAccounts(BaseHandler):
    async def get(self):
        curr_page = int(self.get_argument('curr_page', 1))
        page_num = int(self.get_argument('page_num', 10))
        arg = dict(curr_page=curr_page, page_num=page_num)

        @self.validate_arg(['curr_page', 'page_num'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.queryAccounts(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)


class deleteAccount(BaseHandler):
    async def post(self):
        arg = self.to_dict(self.request.body)

        @self.validate_arg(['account_id'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.deleteAccount(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)


class getOrAddMoney(BaseHandler):
    async def post(self):
        arg = self.to_dict(self.request.body)

        @self.validate_arg(['account_id', 'money'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.getOrAddMoney(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)


class transMoney(BaseHandler):
    async def post(self):
        arg = self.to_dict(self.request.body)

        @self.validate_arg(['out_account_id', 'in_account_id', 'money'], arg)
        def handler(): return 1
        result = handler()
        result = await self.ctrl_index.transMoney(arg) if 200 == result['code'] else 1
        self.finish_ok(**result)

