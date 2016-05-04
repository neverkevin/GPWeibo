# -*- coding: utf-8 -*-

from base_object import BaseObject


class Contents(BaseObject):

    table = 'weibo'
    collection = 'content'
    keyMapping = (
            'wid', 'content', 'ct_date', 'ct_time',
            'attitude', 'repost', 'comment'
        )
    def __init__(self, data=None):
        self.wid = 0
        self.content = ''
        self.ct_date = ''
        self.ct_time = ''
        self.attitude = 0
        self.repost = 0
        self.comment = 0

        BaseObject.__init__(self, data)
