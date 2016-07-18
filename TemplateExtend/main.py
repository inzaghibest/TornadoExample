__author__ = 'zhangxp'
#总之，模块允许你在模板中渲染格式化数据时非常灵活，同时也让你能够只在调用模块时包含指定的一些额外的样式和函数规则。
import os.path
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import pymongo
import json

from tornado.options import define,options
define("port", default=3000, help="give a port", type=int)

#UI模块.
class helloModule(tornado.web.UIModule):
    def render(self, *args, **kwargs):
        return '<h1>Zhang XP\'s BookStore:</h1>'

class BookModule(tornado.web.UIModule):
    def render(self,book):
        return self.render_string('modules/book.html', book = book)
    #在页面中嵌入javascript代码
    #def embedded_javascript(self):
    #    return "alert(\"hi!\")"
   # 比如，你可以添加一个额外的本地CSS文件如下：
    #def css_files(self):
    #return "/static/css/newreleases.css"
    #或者你可以取得一个外部的JavaScript文件：
    #def javascript_files(self):
    #   return "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.14/jquery-ui.min.js"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #生命UI模块,方法:类名 类里定义了返回的内容
            ui_modules={'hello':helloModule, 'Book':BookModule},
            debug=True,
        )
        # 在App初始化时初始化db连接，并给self.db赋值,这样在所有继承web.RequestHandler类的方法中可以使用此db
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["bookstore"]
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #在所有继承RequestHandler的类中使用此db
        coll = self.application.db.books
        books = coll.find()
        self.render(
            "main.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            books = books
            # books=[
            #     {
            #         "title":"Programming Collective Intelligence",
            #         "subtitle": "Building Smart Web 2.0 Applications",
            #         "image":"/static/images/1.jpg",
            #         "author": "Toby Segaran",
            #         "date_added":1310248056,
            #         "date_released": "August 2007",
            #         "isbn":"978-0-596-52932-1",
            #         "description":"<p>This fascinating book demonstrates how you "
            #             "can build web applications to mine the enormous amount of data created by people "
            #             "on the Internet. With the sophisticated algorithms in this book, you can write "
            #             "smart programs to access interesting datasets from other web sites, collect data "
            #             "from users of your own applications, and analyze and understand the data once "
            #             "you've found it.</p>"
            #     }
            # ]
        )
if __name__ == '__main__':
    tornado.options.parse_command_line()
    # app = tornado.web.Application(
    #     handlers=[(r"/", IndexHandler)],
    #     template_path=os.path.join(os.path.dirname(__file__), "templates"),
    #     static_path=os.path.join(os.path.dirname(__file__), "static")
    # )
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

