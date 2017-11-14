#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser


def getDBConf():
    '''
    >>> getDBConf()
    <Storage...>
    '''
    config = configparser.ConfigParser()
    config.read('conf/db.ini')
    return config['db']
    # with open('conf/db.ini', 'r') as cfg_file:
    #    conf.host = config.get('db', 'host')
    #    conf.port = config.get('db', 'port')
    #    conf.db_name = config.get('db', 'db_name')
    #    conf.user = config.get('db', 'user')
    #    conf.password = config.get('db', 'password')
    # return conf


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
