# -*-coding:utf-8-*-
# __author__='admin'
# coding: gb2312
import os
import requests
import urllib2
from bs4 import BeautifulSoup
import zlib
import pickle
from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient



# MongoDB 数据库缓存
'''
class MongoCache(object):

    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = MongoClient('localhost', 27017)
        self.db = client.cache
        self.db.webpage.creat_index('timestamp', expiresAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + 'does not exist')

    def __setitem__(self, url, result):
        record = {'result': Binary(zlib.compress(pickle.dumps(result))),
                  'timestamp': datetime.utcnow()
                  }
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)


mongo_cache = MongoCache(expires=timedelta())

'''
# 网页下载器
class Downloader(object):

    def __init__(self, pathname=None, user_agent='Mozzila/5.0', num_retries=3, cache=None):
        assert isinstance(pathname, object)
        self.pathname = pathname
        self.user_agent = user_agent
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):

        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 < result['code'] < 600:
                    result = None
        if result is None:
            # 设置用户代理
            headers = {'User-Agent': self.user_agent,
                       'Referer': url
                       }
            result = self.download(url, headers, self.num_retries)
            if self.cache:
                self.cache[url] = result

        return result

    def download(self, url, headers=None, proxies=None, num_retries=3):

        print "Downloading:", url
        # 设置用户代理,代理
        user_agent = 'Mozzila/5.0'
        headers = {'User-Ageht': user_agent,
                   'Referer': url
                   }

        try:
            html = requests.get(url, headers=headers, verify=True)
        except urllib2.HTTPError as e:
            print 'Download Eerro:', e.reason
            html = None
            # 若错误序号在500-600之间，重试几次
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    return self.download(url, headers, num_retries - 1)

        return html

    def mkdir(self, path):
        # type: (object, object) -> object
        path = path.strip()
        isExists = os.path.exists(os.path.join('D:/PythonSpider', path))
        if not isExists:
            print '建立文件夹:', path
            os.makedirs(os.path.join('D:/PythonSpider', path))
            os.chdir(os.path.join('D:/PythonSpider' + '/', path))
            return True
        else:
            print '已有此文件'
            return False


if __name__ == '__main__':
    url = 'http://www.baidu.com'
    D = Downloader()
    spider = D(url).text
    soup = BeautifulSoup(spider, 'lxml')

    print soup.prettify()

