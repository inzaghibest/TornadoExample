__author__ = 'zhangxp'

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import textwrap

from tornado.options import define,options
define("port",default=8000,help="give port to server!",type=int)
define("url",default="127.0.0.1",help="give url to http",type=list)

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])
class WrapHandler(tornado.web.RequestHandler):
     def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    #正则表达式告诉Tornado匹配任何以字符串/reverse/开始并紧跟着一个或多个字母的路径。括号的含义是让Tornado保存匹配括号里面表达式的字符串，
    # 并将其作为请求方法的一个参数传递给RequestHandler类。
    app = tornado.web.Application(handlers=[(r"/reverse/(\w+)", ReverseHandler),
         (r"/wrap", WrapHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


