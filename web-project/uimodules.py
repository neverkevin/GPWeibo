#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado


class Main(tornado.web.UIModule):
    def render(self, tags):
        return self.render_string('header.html', tags=tags)


class MainNav(Main):
    def render(self, url):
        tags = [
                {'name': '首页', 'url': '/'},
                {'name': '旅游倾向', 'url': '/sights'},
                {'name': '用户数据', 'url': '/user'},
            ]
        for tag in tags:
            if tag['url'] == url:
                tag['active'] = True
        return Main.render(self, tags)
