# -*-coding:utf-8-*-
# __author__='admin'
# coding:utf-8
# coding:gb2312
import os
from download import Downloader
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

D = Downloader()


class MzituSpider(object):
    def __init__(self):
        pass

    def all_url(self, start_url):
        html = D(start_url).text
        soup = BeautifulSoup(html, "lxml")
        a_list = soup.find('div', class_='all').find_all('a')

        for a in a_list:
            title = a.get_text()
            print "开始保存:", title
            path = str(title).replace('?', '_')
            self.mkdir(path)

            href = a['href']
            self.html(href)

    def html(self, href):
        # 获取套图的最大张数
        page_html = D(href).text
        page_soup = BeautifulSoup(page_html, "lxml")
        max_span = page_soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span)+1):
            page_url = href+'/'+str(page)
            self.img(page_url)

    def img(self, page_url):
        # 获取图片
        img_html = D(page_url).text
        img_soup = BeautifulSoup(img_html, "lxml")
        img_url = img_soup.find('div', class_='main-image').find('img')['src']
        self.save(img_url)

    def save(self, img_url):
        # 将图片存入文件中
        name = img_url[-9:-4]
        img = D(img_url)
        f = open(name+'.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):
        path = path.strip()
        uipath = unicode(path, "utf8")
        existment = os.path.exists(os.path.join('D:/mzitu/pictures', uipath))
        if not existment:
            print '建立文件夹，名为：',path
            os.makedirs(os.path.join('D:/mzitu/pictures', uipath))
            os.chdir(os.path.join('D:/mzitu/pictures', uipath))
            return True
        else:
            print '此文件已存在。'
            return False


if __name__ == '__main__':
    start_url = 'http://www.mzitu.com/old'
    Spider1 = MzituSpider()
    Spider1.all_url(start_url=start_url)