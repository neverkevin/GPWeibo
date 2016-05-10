# -*- coding: utf-8 -*-

import json
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    @property
    def redis(self):
        """An alias for `self.application.redis`."""
        return self.application.redis

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        return username and username or None

    def set_cache(self, key, value):
        self.redis.set(key, value)

    def is_req_cached(self, key):
        cached_result = self.redis.get(key)
        if cached_result:
            return True, json.loads(cached_result)
        return False, None
