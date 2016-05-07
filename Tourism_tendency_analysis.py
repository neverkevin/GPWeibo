#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import jieba
import codecs
import threading
from Queue import Queue
from crawler.GPCrawler.dal import MongoDal
reload(sys)
sys.setdefaultencoding('utf8')


class TaskLoader(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self, name='loader')
        self.worker_queue = params.get('worker_queue')
        self.db = params.get('db')
        self.daemon = True

    def run(self):
        contents = self.db.find('weibo', 'contents')
        for content in contents:
            self.worker_queue.put(content)


class Analyst(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self, name='analyst')
        self.worker_queue = params.get('worker_queue')
        self.analysis_queue = params.get('analysis_queue')
        self.db = params.get('db')
        self.sights = params.get('sights')
        self.daemon = True

    def run(self):
        while True:
            content = self.worker_queue.get()
            if content is None:
                continue
            sight_list = self.analysis(content)
            if sight_list is None:
                continue
            for sight in sight_list:
                self.analysis_queue.put(sight)

    def analysis(self, content):
        sights = self.sights
        word_list = self.cut_words(content['content'])
        intersection = set(word_list).intersection(set(sights))
        if intersection == set([]):
            return None
        pub_date = self.get_put_date(content['ct_date'], content['ct_time'])
        sight_list = list()
        for sight in intersection:
            sight_list.append(dict(
                wid=content['wid'],
                sight=sight,
                year=pub_date['year'],
                month=pub_date['month'],
                day=pub_date['day'],
                hour=pub_date['hour'],
                minutes=pub_date['minutes']
                ))
        return sight_list

    def cut_words(self, content):
        words = jieba.cut(content, cut_all=False)
        return [word for word in words]

    def get_put_date(self, date, time):
        date_list = date.split('-')
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        time_list = time.split(':')
        hour = time_list[0]
        minutes = time_list[1]
        return dict(
                year=int(year),
                month=int(month),
                day=int(day),
                hour=int(hour),
                minutes=int(minutes)
            )


class ResultSaver(threading.Thread):
    def __init__(self, params):
        threading.Thread.__init__(self, name='saver')
        self.analysis_queue = params.get('analysis_queue')
        self.db = params.get('db')
        self.daemon = True

    def run(self, ):
        while True:
            sight = self.analysis_queue.get()
            self.saver(sight)

    def saver(self, sight):
        user_info = self.db.find_one('weibo', 'user', {'wid': sight['wid']})
        sight['name'] = user_info['name']
        sight['area'] = user_info['area']
        self.db.insert_one(
                'weibo', 'sights_tendency', sight
                )
        print 'analysed: name %s, area %s, sight %s' % (
                sight['name'],
                sight['area'],
                sight['sight']
            )


if __name__ == '__main__':
    worker_queue = Queue(5000000)
    analysis_queue = Queue(3000)
    with codecs.open('sight.txt', 'r', 'utf-8') as f:
        sights = f.read()
    sights = sights.split('\n')
    db = MongoDal()
    para_dict = dict(
            worker_queue=worker_queue,
            analysis_queue=analysis_queue,
            sights=sights,
            db=db,
        )
    threads = []
    threads.append(TaskLoader(para_dict))
    for i in range(10):
        threads.append(Analyst(para_dict))
    for i in range(5):
        threads.append(ResultSaver(para_dict))
    for t in threads:
        t.start()
    while True:
        print 'worker size: %s, analyst size: %s ' % (
                worker_queue.qsize(),
                analysis_queue.qsize()
            )
        time.sleep(10)
