#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db_bz import engine, session
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, DateTime

Base = declarative_base(bind=engine)


class OauthInfo(Base):
    '''
    oauth_info 登录的用户信息
    >>> OauthInfo.__table__.create(checkfirst=True)
    '''
    __tablename__ = 'oauth_info'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # 建立时间
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow)  # update 时间

    out_id = Column(Text, nullable=False)  # 外部的id
    type = Column(Text, nullable=False)  # oauth 类型, twitter github
    name = Column(Text, nullable=False)
    avatar = Column(Text, nullable=False)  # 头像
    email = Column(Text)
    location = Column(Text)  # 归属地


def addTest():
    '''
    # >>> addBaseTest()
    '''
    for i in range(0, 10):
        base = Base()
        session.add(base)
    session.commit()


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
