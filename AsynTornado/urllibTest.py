__author__ = 'zhangxp'
#urllib
import urllib.request

if __name__ == '__main__':
    # 1.最简单的
    # f = urllib.request.urlopen('http://www.baidu.com')
    # text = f.read()
    # print(text)
    # 2.使用request
    # response = urllib.request.Request('http://www.qq.com')
    # req = urllib.request.urlopen(response)
    # mytext = req.read()
    # print(mytext)
    # 3.发送数据
    url = 'http://localhost/login.php'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {
    'act' : 'login',
    'login[email]' : 'yzhang@i9i8.com',
    'login[password]' : '123456'
    }
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data)
    req.add_header('Referer', 'http://www.python.org/')
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print(the_page.decode("utf8"))


