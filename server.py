# coding: utf8
from tornado import web
from tornado import ioloop
from tornado.options import options, define
from conf import op_conf
import route
import json
import logging
import models
import os

define("port", default=8880, help='default port', type=int)
define('debug', default=True, type=bool)
define('dev', default=True, type=bool)
options.parse_command_line()

settings = dict(
    gzip=True,
    debug=options.debug,
    cookie_secret="123",
    xsrf_cookies=False,
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
)


class Application(web.Application):
    def log_request(self, handler):
        if 'log_function' in self.settings:
            self.settings['log_function'](handler)
            return
        if handler.get_status() < 400:
            log_method = logging.info
        elif handler.get_status() < 500:
            log_method = logging.warning
        else:
            log_method = logging.error
        request_time = 1000.0 * handler.request.request_time()
        params = handler.request.body.decode("utf-8")
        if params.strip() != '':
            try:
                params = json.loads(params)
            except json.decoder.JSONDecodeError:
                params = {}
        else:
            params = {}
        log_method(
            "%d %s %s (%s) %.2fms params=%s",
            handler.get_status(),
            handler.request.method,
            handler.request.uri,
            handler.request.headers.get("X-Real-Ip", "127.0.0.1"),
            request_time,
            params
        )


def main():
    try:
        models.create_table()
    except:
        print('table has exits')
    op_conf.chang_conf(options.dev)
    app = Application(route.url_route, **settings)
    app.listen(options.port)
    print("server is listening on http://127.0.0.1:%s" % options.port)
    io_loop = ioloop.IOLoop.instance()
    io_loop.start()


if __name__ == '__main__':
    main()
