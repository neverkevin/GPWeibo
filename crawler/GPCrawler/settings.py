# -*- coding: utf-8 -*-

USERS = {
            'username': 'daola0761692@163.com',
            'password': 'aaa333'
        }

HOST = "weibo.cn"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
REFERER = 'http://weibo.cn'
# REFERER = "http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459153356.0121&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16",

CRAWL_PAGE = 3
DOWNLOAD_DELAY = [0.5, 1, 2, 3]
REDIS_QUEUE = True

ACCOUNT_TABLE = 'accuont'
# mysql config
MYSQL_HOST = 'localhost'
MYSQL_DATABASE_NAME = 'weibo'
MYSQL_USER_NAME = 'root'
MYSQL_PASS_WORD = 'ssdut'

# mongo config
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# redis config
REDIS_ADDRESS = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWD = 'ssdut'
REDIS_INDEX = 1
