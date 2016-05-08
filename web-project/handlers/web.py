# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
from operations.routes import route
from base_handler import BaseHandler


@route(r'/user$', name='user')
class UserHandler(BaseHandler):
    def get(self):
        db = self.mongo_db.weibo
        user_count = db.user.count()
        contents_count = db.contents.count()
        users = db.user.find()
        self.render('user.html', users=users, cc=contents_count, uc=user_count)


@route(r'/user/\d+$', name='twits')
class UsercontentHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        wid = re.findall('\d+$', url)[0]
        db = self.mongo_db.weibo
        contents = db.contents.find({'wid': str(wid)})
        self.render('user_contents.html', contents=contents)


@route(r'/show$', name='show')
class ShowHandler(BaseHandler):
    def get(self):
        self.render('sights_dentency.html')
