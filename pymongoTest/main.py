__author__ = 'zhangxp'

# 可以像访问对象或者字典的方式访问一个数据库,字典：一个数据库名对应一个数据库
# import pymongo
# conn = pymongo.Conncection("locahost", 27017)
# db = conn.example or: db = conn['example']
#一个数据库有多个集合
# db.collection_names()
# 创建集合 widgets类似于一个表的集合,而一个文档类似于一个表
#widgets = db.widgets or: widgets = db['widgets']
#向集合中插入数据
#widgets.insert({"foo":"bar"}) 可以理解为键值为字段名,值为字段的值.
#db.widgets.save(doc) 类似于提交

#代码清单4-1 一个词典Web服务：definitions_readonly.py
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, debug=True)

#一旦我们在Application对象中添加了db属性，我们就可以在任何RequestHandler对象中使用self.application.db访问它
class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})
    def post(self, word):
        define = self.get_argument("definetion")
        coll = self.application.db.words
        word_doc = coll.find_one({"word":word})
        if word_doc:
            word_doc["define"] = define
            coll.save(word_doc)
        else:
            word_doc = coll.insert({"word":word, "define":define})
            coll.save(word_doc)
        del word_doc["_id"]
        self.write(word_doc)




if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

