#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def getDBConf():
    '''
    >>> getDBConf()
    <Section: db>
    '''
    config = configparser.ConfigParser()
    config.read('conf/db.ini')
    return config['db']


def getEngine():
    '''
    >>> getEngine()
    Engine(...
    '''

    db_conf = getDBConf()
    connect_str = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
        db_conf['user'],
        db_conf['password'],
        db_conf['host'],
        db_conf['port'],
        db_conf['db_name'],
    )
    engine = create_engine(connect_str)
    return engine


def query(sql):
    conn = getEngine().connect()
    stmt = text("SELECT * FROM oauth_info")
    print(conn.execute(stmt).fetchall())


if __name__ == '__main__':
    query('123')
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
