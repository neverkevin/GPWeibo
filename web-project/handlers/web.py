# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
from tornado import gen
from base_handler import BaseHandler
from models import model
from operations.routes import route

COLORS = ['EE1601', 'D88101', '2F9D66', '78BA01']


@route(r'/', name='index')
class MainHander(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('index.html', url=url)


@route(r'/user$', name='user')
class UserHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        url = self.request.uri
        users = yield model.get_users()
        user_count, contents_count = yield model.get_count()
        self.render(
            'user.html', users=users, cc=contents_count,
            uc=user_count, url=url
            )


@route(r'/user/\d+$', name='twits')
class UsercontentHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        url = self.request.uri
        wid = re.findall('\d+$', url)[0]
        contents = yield model.get_user_contents({'wid': str(wid)})
        self.render('user_contents.html', contents=contents)


@route(r'/sights$', name='show')
class ShowHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('sights_dentency.html', url=url)

    @gen.coroutine
    def post(self):
        data = self.request.arguments
        query = get_query_filter(data)
        sights = yield model.query_sights(query)
        color = dict()
        for s in sights:
            color[s] = random.choice(COLORS)
        weight = [[s, 8+i] for i, s in enumerate(sights)]
        self.write(dict(color=color, weight=weight))


def get_query_filter(data):
    area = data.get('area', [''])[0]
    month = data.get('month', [''])[0]
    time = data.get('time', [''])[0]
    query = dict()
    time_filter = get_time_shuttle(time)
    if area:
        query['area'] = area
    if month:
        query['month'] = int(month)
    if time_filter:
        query.update(time_filter)
    return query


def get_time_shuttle(time):
    if not time:
        return None
    elif time == 'morning':
        return {'hour': {'$gt': 6, '$lte': 10}}
    elif time == 'noon':
        return {'hour': {'$gt': 10, '$lte': 14}}
    elif time == 'afternoon':
        return {'hour': {'$gt': 14, '$lte': 19}}
    elif time == 'evening':
        return {'$or': [{'hour': {'$gt': 19}}, {'hour': {'$lte': 6}}]}
