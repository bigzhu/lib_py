#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback


def getExpInfoAll(just_info=False):
    '''
    得到Exception的异常
    >>> getExpInfoAll()
    'NoneType: None...'
    '''
    if just_info:
        info = sys.exc_info()
        return str(info[1])
    else:
        return traceback.format_exc()


def getExpInfo():
    '''
    得到Exception的异常, 只显示错误信息
    >>> getExpInfo()
    'None'
    '''
    return getExpInfoAll(True)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
