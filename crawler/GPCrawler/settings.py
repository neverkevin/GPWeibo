# -*- coding: utf-8 -*-

HOST = "weibo.cn"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
REFERER = 'http://weibo.cn'
# REFERER = "http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459153356.0121&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16",

CRAWL_PAGE = 25
DOWNLOAD_DELAY = [0.5, 1, 2, 3, 4]
REDIS_QUEUE = True

ACCOUNT_TABLE = 'account'
# mysql config
MYSQL_HOST = 'localhost'
MYSQL_DATABASE_NAME = 'weibo'
MYSQL_USER_NAME = ''
MYSQL_PASS_WORD = ''

# mongo config
MONGO_HOST = ''
MONGO_PORT = 27017
MONGO_USER = ''
MONGO_PASSWD = ''

# redis config
REDIS_ADDRESS = ''
REDIS_PORT = '6379'
REDIS_PASSWD = ''
REDIS_INDEX = 1
