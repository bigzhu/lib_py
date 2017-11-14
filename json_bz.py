#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import time
import decimal


class ExtEncoderNew(json.JSONEncoder):

    '''
    datetime 直接取出来
    try this: from bson import json_util print json.dumps(user, default=json_util.default)
    modify by bigzhu at 15/01/30 11:25:22 增加对 utils.IterBetter 的支持
    '''

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, datetime.time):
            # print {'HH': o.strftime('%H'), 'mm': o.strftime('%M'), 'ss': o.strftime('%S')}
            return o.strftime('%H:%M:%S')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        # elif isinstance(o, utils.IterBetter):
        #    return list(o)
        else:
            print(o)
            print(type(o))
            raise Exception('json 无法格式化这个数据类型')
        # Defer to the superclass method
        return json.JSONEncoder(self, o)


class ExtEncoder(json.JSONEncoder):

    '''
    modify by bigzhu at 15/01/30 11:25:22 增加对 utils.IterBetter 的支持
    '''

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return time.mktime(o.timetuple()) * 1000
        if isinstance(o, datetime.time):
            # return {'HH': o.strftime('%H'), 'mm': o.strftime('%M'), 'ss': o.strftime('%S')}
            return o.strftime('%H:%M:%S')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        # elif isinstance(o, utils.IterBetter):
        #    return list(o)
        else:
            raise Exception('json 无法格式化这个数据类型')
        # Defer to the superclass method
        return json.JSONEncoder(self, o)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
