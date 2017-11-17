#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def getExecutingPath():
    '''
    返回当前执行的 python 文件所在路径
    >>> getExecutingPath()
    '/Users/bigzhu/lib_py'
    '''
    # return
    # os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # script directory
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return dirname


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
