__author__ = 'zhangxp'

import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.gen

import urllib
import json
import datetime
import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    #@tornado.web.asynchronous装饰器来告诉Tornado保持连接开启
    @tornado.web.asynchronous
    @tornado.gen.engine

    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        values = {"q": query, "result_type": "recent", "rpp": 100}
        #AsyncHTTPClient的fetch方法并不返回调用的结果。取而代之的是它指定了一个callback参数；你指定的方法或函数将在HTTP请求完成时被调用，
        # 并使用HTTPResponse作为其参数。
        response = yield tornado.gen.Task(client.fetch, "http://search.twitter.com/search.json?" + \
                urllib.parse.urlencode(values))
        body = json.loads(response.body)
        result_count = len(body['results'])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['results'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                "%a, %d %b %Y %H:%M:%S +0000")
        seconds_diff = time.mktime(now.timetuple()) - \
                time.mktime(oldest_tweet_at.timetuple())
        tweets_per_second = float(result_count) / seconds_diff
        self.write("""
<div style="text-align: center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 24px">tweets per second</div>
</div>""" % (self.query, tweets_per_second))
        #记住当你使用@tornado.web.asynchonous装饰器时，Tornado永远不会自己关闭连接。你必须在你的RequestHandler对象中调用finish方法来显式地告诉Tornado关闭连接
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
