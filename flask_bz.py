#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.json import JSONEncoder
from json_bz import encodeJson


class ExtEncoder(JSONEncoder):
    '''
    扩展 flask 的encode 方法
    '''
    def default(self, o):
        return encodeJson(o, super(ExtEncoder, self).default)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
