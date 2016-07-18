__author__ = 'zhangxp'
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            title="Home Page",
            header="Books that are great",
            books=[
                "Learning Python",
                "Programming Collective Intelligence",
                "Restful Web Services"
            ]
        )

# 在双大括号中的单词是占位符，当我们渲染模板时希望以实际值代替。我们可以使用向render函数中传递关键字参数的方法指定什么值将被填充到HTML文件中的对应位置，
# 其中关键字对应模板文件中占位符的名字。下面是在PoemPageHandler中相应的代码部分：
class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', PoemPageHandler)],
    # 那么有什么不一样的地方呢？首先，我们向Application对象的__init__方法传递了一个template_path参数。
    # template_path=os.path.join(os.path.dirname(__file__), "templates")
    # template_path参数告诉Tornado在哪里寻找模板文件。我们将在本章和第三章中讲解其确切性质和语法，而它的基本要点是：模板是一个允许你嵌入Python代码片段的HTML文件。
    # 上面的代码告诉Python在你Tornado应用文件同目录下的templates文件夹中寻找模板文件。
    # 一旦我们告诉Tornado在哪里找到模板，我们可以使用RequestHandler类的render方法来告诉Tornado读入模板文件，插入其中的模版代码，并返回结果给浏览器。
    # 比如，在IndexHandler中，我们发现了下面的语句：
    # self.render('index.html')
    # 这段代码告诉Tornado在templates文件夹下找到一个名为index.html的文件，读取其中的内容，并且发送给浏览器。
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()