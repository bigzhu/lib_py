#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from sqlalchemy import create_engine
# from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
engine = None


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

    global engine
    if engine is not None:
        return engine

    db_conf = getDBConf()
    connect_str = "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
        db_conf['user'],
        db_conf['password'],
        db_conf['host'],
        db_conf['port'],
        db_conf['db_name'],
    )
    engine = create_engine(connect_str, echo=False)

    return engine


def getSession():
    '''
    >>> getSession()
    <sqlalchemy.orm.session.Session object at ...
    '''
    engine = getEngine()
    Session = sessionmaker(bind=engine)
    return Session()


# def query(sql):
#    '''
#    >>> query('123')
#    '''
#    conn = getEngine().connect()
#    stmt = text("SELECT * FROM oauth_info")
#    conn.execute(stmt).fetchone()


if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
