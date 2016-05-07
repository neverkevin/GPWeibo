# -*- coding: utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    @property
    def mysql_db(self):
        """An alias for `self.application.mysql_db`."""
        return self.application.mysql_db

    @property
    def mongo_db(self):
        """An alias for `self.application.mongo_db`."""
        return self.application.mongo_db

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        return username and username or None
