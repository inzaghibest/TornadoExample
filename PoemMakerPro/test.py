__author__ = 'zhangxp'
from tornado.template import  Template

print(Template("{{ 1+1 }}").generate())
