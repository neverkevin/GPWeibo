# -*- coding: utf-8 -*-

from base_object import BaseObject


class Contents(BaseObject):

    table = 'contents'
    keyMapping = (
            'content', 'ct_date', 'ct_time', 'attitude',
            'repost', 'comment',
        )

    def __init__(self, data=None):
        self.content = ''
        self.ct_date = ''
        self.ct_time = ''
        self.attitude = ''
        self.repost = ''
        self.comment = ''

        BaseObject.__init__(self, data)
