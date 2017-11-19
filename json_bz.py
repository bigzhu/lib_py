#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import decimal
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper


class ExtEncoder(json.JSONEncoder):
    '''
    datetime 直接用标准格式化
    try this: from bson import json_util print json.dumps(user, default=json_util.default)
    modify by bigzhu at 15/01/30 11:25:22 增加对 utils.IterBetter 的支持
    '''

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(
                o, datetime.date) or isinstance(o, datetime.time):
            return o.isoformat()
        elif isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o.__class__, DeclarativeMeta):
            columns = [c.key for c in class_mapper(o.__class__).columns]
            return dict((c, getattr(o, c)) for c in columns)
        else:
            print(o)
            print(type(o))
            raise Exception('json 无法格式化这个数据类型')
        # Defer to the superclass method
        return json.JSONEncoder(self, o)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
