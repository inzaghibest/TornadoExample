__author__ = 'zhangxp'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# Tornado包括了一个有用的模块（tornado.options）来从命令行中读取设置。我们在这里使用这个模块指定我们的应用监听HTTP请求的端口。它的工作流程如下：
# 如果一个与define语句中同名的设置在命令行中被给出，那么它将成为全局options的一个属性。如果用户运行程序时使用了--help选项，程序将打印出所有你定
# 义的选项以及你在define函数的help参数中指定的文本。如果用户没有为这个选项指定值，则使用default的值进行代替。Tornado使用type参数进行基本的参数
# 类型验证，当不合适的类型被给出时抛出一个异常。因此，我们允许一个整数的port参数作为options.port来访问程序。如果用户没有指定值，则默认为8000。
# python HelloTornado.py --port=8000 --url=http://127.0.0.1 &
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

if __name__ == "__main__":
    #tornado.options解析命令行
    tornado.options.parse_command_line()
    #告诉tornado哪个类相应请求,/在根目录相应请求
    #handlers:
    #它应该是一个元组组成的列表，其中每个元组的第一个元素是一个用于匹配的正则表达式，第二个元素是一个RequestHanlder类。
    # 在hello.py中，我们只指定了一个正则表达式-RequestHanlder对，但你可以按你的需要指定任意多个
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    # 从这里开始的代码将会被反复使用：一旦Application对象被创建，我们可以将其传递给Tornado的HTTPServer对象，然后使用我们在命令行指定的端口进行监听
    # （通过options对象取出。）最后，在程序准备好接收HTTP请求后，我们创建一个Tornado的IOLoop的实例。
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()