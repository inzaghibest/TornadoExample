__author__ = 'zhangxp'
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
from uuid import uuid4

from tornado.options import define,options
define("port", default=8000, help="give a port", type=int)

class ShoppingCart(object):
    totalInventory = 10 # 初始存货总数
    callbacks = [] # 回调函数列表
    carts = {} # 购物车sessions

    #获取存货数量
    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

    #注册一个回调函数
    def register(self, callback):
        print("注册了一个回调函数")
        self.callbacks.append(callback)

    #添加一个元素
    def moveItemToCart(self, session):
        if session in self.carts:
            return
        self.carts[session] = True
        self.notifyCallbacks()

    #删除一个元素
    def removeItemFromCart(self, session):
        if session not in self.carts:
            return
        del(self.carts[session])
        self.notifyCallbacks()

    #回调函数执行
    def callbackHelper(self, callback):
        callback(self.totalInventory)

    #我们只需要将回调函数列表替换为一个新的空列表。在请求处理中被调用并完成后删除已注册的回调函数十分重要，因为随后在调用回调函数时将在
    # 之前已关闭的连接上调用finish()，这会产生一个错误
    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)
        self.callbacks = []
        print("notify over")

class DetailHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #为每个链接产生一个唯一标识
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render('index.html',session=session,count=count)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        print("处理post请求")
        action = self.get_argument('action')
        session = self.get_argument('session')
        if not session:
            self.set_status(400)
            return

        if action == 'add':
            print("添加到购物车")
            self.application.shoppingCart.moveItemToCart(session)
            print("Postmove 结束")
        elif action == 'remove':
            print("从购物车移除")
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)

            print("Post结束")

#每当一个页面连接,注册一个异步回调函数,当操作购物车时调用回调函数.
class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.on_message)
    def on_message(self, count):
        self.write('{"inventoryCount":"%d"}' % count)
        print('{"inventoryCount":"%d"}' % count)
        print("ok")
        self.finish()
        print("ok")


class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
   tornado.options.parse_command_line()

   app = Application();
   http_server = tornado.httpserver.HTTPServer(app)
   http_server.listen(options.port)
   tornado.ioloop.IOLoop.instance().start()


