#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import datetime
import decimal
import model_bz
#from sqlalchemy.util._collections import AbstractKeyedTuple


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
        # ! 貌似没有用, 直接按 tuple 去解析了
        # tuple 是基础结构类型, 在 _iterencode 里转换了, 没法在这里定义转换
        #elif isinstance(o, AbstractKeyedTuple):
        #    return o._asdict()
        elif isinstance(o, model_bz.Base):
            # return o.__dict__
            return {c.name: getattr(o, c.name, None) for c in o.__table__.columns}
        else:
            print(o)
            print(type(o))
            raise Exception('json 无法格式化这个数据类型')
        return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
