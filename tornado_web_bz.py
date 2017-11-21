#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 tornado 的公用 web api, 这里对应以前的 web_bz
'''
import tornado
import tornado.websocket
import tornado.web
import json
import oauth_bz

from tornado_bz import BaseHandler
import tornado_bz
import json_bz
import db_bz
from model_bz import OauthInfo


class api_oauth_info(BaseHandler):
    '''
    取 get_oauth_info 用户信息
    '''

    @tornado_bz.handleErrorJson
    @tornado_bz.mustLoginJson
    def get(self):
        """
        @apiGroup public
        @api {get} /api_oauth_info 取 oauth 登录的用户信息 api_oauth_info
        @apiSuccess {Number} id id
        @apiSuccess {String} created_at 生成日期
        @apiSuccess {String} updated_at 更新日期
        @apiSuccess {String} out_id 外部系统的id
        @apiSuccess {String} type 外部系统的类型
        @apiSuccess {String} name 用户名
        @apiSuccess {String} avatar 头像
        @apiSuccess {String} email 邮件
        @apiSuccess {String} location 位置
        @apiSuccessExample {json} Success-Response:
        {
        "id": 5,
        "created_at": "2017-05-24T22:43:26.799664",
        "updated_at": "2017-05-24T22:43:26.799664",
        "out_id": "73B15F4A285048EB28AD25B26D01207F",
        "type": "qq",
        "name": "bigzhu",
        "avatar": "http://q.qlogo.cn/qqapp/101318491/73B15F4A285048EB28AD25B26D01207F/100",
        "email": null,
        "location": "云南昆明"
        }
        """
        self.set_header("Content-Type", "application/json")
        user_id = self.current_user
        session = db_bz.getSession()
        oauth_infos = session.query(OauthInfo).filter(OauthInfo.id == int(user_id)).all()

        if not oauth_infos:
            raise Exception('没有用户' + user_id)
        self.write(json.dumps(oauth_infos[0], cls=json_bz.ExtEncoder))


class web_socket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        message = json.loads(message)
        if message['oper'] == 'register':
            print('register')
            self.registerSocket(message['key'])
        self.write_message(json.dumps({'error': '0'}))

    def on_close(self):
        print("WebSocket closed")
        the_name = 'sockets'
        if self in self.settings[the_name][self.key]:
            print('remove current socket')
            self.settings[the_name][self.key].remove(self)

    def registerSocket(self, key):
        self.key = key
        the_name = 'sockets'
        if self.settings.get(the_name) is None:
            self.settings[the_name] = {}
        if self.settings[the_name].get(key) is None:
            self.settings[the_name][key] = []
        self.settings[the_name][key].append(self)
        print(self.settings[the_name])


class qq(BaseHandler, oauth_bz.QQAuth2Minix):
    def initialize(self):
        BaseHandler.initialize(self)

    @tornado.web.asynchronous
    def get(self):
        redirect_uri = self.settings["qq_redirect_uri"]
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=self.settings["qq_api_key"],
                client_secret=self.settings["qq_api_secret"],
                code=self.get_argument("code"),
                extra_fields={"grant_type": "authorization_code"},
                callback=self._on_auth)
            return
        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=self.settings["qq_api_key"],
            extra_params={
                "response_type": "code"
            })

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "qq auth failed")
        self.openid = user.get("openid", 0)
        if user.get("ret", 0) or not self.openid:
            self.render('error.html', msg=user.get('msg', 'error'))
        else:
            access_token = user.get('access_token')
            client_id = user.get('client_id')
            self.qq_request("/user/get_user_info", 'GET', self.openid,
                            access_token, client_id, self.saveUserInfo)

    def saveUserInfo(self, user_info):
        '''
        {
            "ret": 0,
            "msg": "",
            "is_lost":0,
            "nickname": "bigzhu",
            "gender": "男",
            "province": "云南",
            "city": "昆明",
            "year": "1983",
            "figureurl": "http:\/\/qzapp.qlogo.cn\/qzapp\/101318491\/73B15F4A285048EB28AD25B26D01207F\/30",
            "figureurl_1": "http:\/\/qzapp.qlogo.cn\/qzapp\/101318491\/73B15F4A285048EB28AD25B26D01207F\/50",
            "figureurl_2": "http:\/\/qzapp.qlogo.cn\/qzapp\/101318491\/73B15F4A285048EB28AD25B26D01207F\/100",
            "figureurl_qq_1": "http:\/\/q.qlogo.cn\/qqapp\/101318491\/73B15F4A285048EB28AD25B26D01207F\/40",
            "figureurl_qq_2": "http:\/\/q.qlogo.cn\/qqapp\/101318491\/73B15F4A285048EB28AD25B26D01207F\/100",
            "is_yellow_vip": "0",
            "vip": "0",
            "yellow_vip_level": "0",
            "level": "0",
            "is_yellow_year_vip": "0"
        }
        '''
        user = json.loads(user_info)

        oauth_info = dict(
            out_id=self.openid,
            type='qq',
            name=user['nickname'],
            avatar=user.get('figureurl_qq_2'),
            email=user.get('email'),
            location=user.get('province') + user.get('city'))

        db_oauth_info = oauth_bz.saveAndGetOauth(oauth_info)
        user_id = str(db_oauth_info[0].id)
        self.set_secure_cookie("user_id", user_id)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
