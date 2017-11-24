#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
tornado 相关的公用代码
'''
import functools
import json
import os

from tornado.web import RequestHandler

import exception_bz
import path_bz

import configparser
config = configparser.ConfigParser()
config.read('conf/config.ini')
cookie_secret = config.get('tornado', 'cookie_secret')


def getSettings():
    '''
        返回 tornado 的 settings ,有一些默认值,省得每次都设置:
            debug:  True 则开启调试模式,代码自动部署,但是有语法错误,会导致程序 cash
            ui_modules 自定义的 ui 模块,默认会引入 tornado_ui_bz
            login_url: 装饰器 tornado.web.authenticated 未登录时候,重定向的网址
    >>> getSettings()
    {'static_path': '/Users/bigzhu/lib_py/static', 'debug': True, 'cookie_secret': ...
    '''
    settings = {
        'static_path': os.path.join(path_bz.getExecutingPath(), 'static'),
        'debug': True,
        'cookie_secret': cookie_secret,
        'autoescape': None,  # 模板自定义转义
        'login_url': "/login"
    }
    return settings


def getURLMap(the_globals):
    '''
        根据定义的tornado.web.RequestHandler,自动生成url map
        modify by bigzhu at 15/03/06 15:53:59 在这里需要设置 lib 的 static, 用于访问 lib 的 static 文件
        create by bigzhu at 16/02/23 18:29:49 剔除多余的lib_static
    >>> web_class = getAllWebBzRequestHandlers()
    >>> getURLMap(web_class)
    [('/BaseHandler', <class 'tornado_bz.BaseHandler'>)...
    '''
    url_map = []
    for i in the_globals:
        try:
            if issubclass(the_globals[i], RequestHandler):
                url_map.append((r'/' + i, the_globals[i]))
                url_map.append((r"/%s/(.*)" % i, the_globals[i]))
        except TypeError:
            continue
    return url_map


def getAllWebBzRequestHandlers():
    '''
    获取当前所有的 RequestHandlers Class Name
    >>> getAllWebBzRequestHandlers()
    {'BaseHandler': <class 'tornado_bz.BaseHandler'>...
    '''
    all_class = {}
    import inspect
    import tornado_web_bz  # 避免交叉 import 错误, 在这里 import
    for name, cls in inspect.getmembers(tornado_web_bz):  # 取出公用的那些 web api
        try:
            if issubclass(cls, RequestHandler):
                all_class[cls.__name__] = cls
        except TypeError:
            pass
    return all_class


def mustLoginJson(method):
    '''
    必须要登录 api
    create by bigzhu at 15/06/21 08:00:56
    '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.get_current_user():
            pass
        else:
            raise Exception('请登录后再操作')
        return method(self, *args, **kwargs)

    return wrapper


def handleErrorJson(method):
    '''
    出现错误的时候,用json返回错误信息回去
    很好用的一个装饰器
    '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")
        try:
            method(self, *args, **kwargs)
        except Exception:
            print(exception_bz.getExpInfoAll())
            self.write(json.dumps({'error': exception_bz.getExpInfo()}))

    return wrapper


def getTName(self, name=None):
    '''
    取得模板的名字
    与类名保持一致
    '''
    if name:
        return 'template/' + name + '.html'
    else:
        return 'template/' + self.__class__.__name__ + '.html'


class BaseHandler(RequestHandler):
    '''
    create by bigzhu at 15/01/29 22:53:07 自定义一些基础的方法
        设置 pg
        设定 current_user 为 cookie user_id
    modify by bigzhu at 15/01/30 09:59:46 直接返回 user_info
    modify by bigzhu at 15/01/30 10:32:37 默认返回 user_info 的拆离出去
    modify by bigzhu at 15/02/21 00:41:23 修改 js_embed 的位置到 </head> 前
    modify by bigzhu at 15/03/06 17:13:21 修改 js_file 的位置到 </head> 前
    modify by bigzhu at 15/06/28 22:37:24 让js_list用一样的次序显示,改回append
    modify by bigzhu at 15/06/28 22:39:29 为了让js_list能在最前,insert location 改为 <head>后
    modify by bigzhu at 15/09/15 10:22:27 删除对render的重载，vue现在没必要插入最前
    modify by bigzhu at 15/09/17 10:31:49 删除多余的重载，为了在lib用ui module;搞得太复杂了
    modify by bigzhu at 16/07/31 15:52:07 也从 headers 里取 Authorization
    '''

    def initialize(self):
        self.template = getTName(self)
        self.data = {'error': '0'}
        RequestHandler.initialize(self)

    def get_current_user(self):
        if self.get_secure_cookie('user_id'):
            return str(self.get_secure_cookie('user_id'), 'utf-8')


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
