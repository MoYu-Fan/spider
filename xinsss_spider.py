# -*-coding:utf-8 -*-
# coding:utf-8
# coding:gb3212
# __author__= 'admin'

from download import Downloader
from bs4 import BeautifulSoup


D = Downloader()
start_url = 'http://www.xinsss999.com/list/index6.html'



class XinSpider(object):
    def __init__(self):
        pass

    def all_urls(self, start_url):
        html = D(start_url).text
        soup1 = BeautifulSoup(html, 'lxml')
        a_list = soup1.find('div', class_="index-tj mb clearfix").find_all('a')
        for a in a_list:
            title = a['title']
            D.mkdir(path=title)
            print '开始保存：', title

            href = 'http://www.xinsss999.com' + a['href']
            self.get_avurls(href)

    def get_avurls(self, href):
        html2 = D(href).text
        soup2 = BeautifulSoup(html2, 'lxml')
        av_urls = soup2.find('div', class_='taba-down mb clearfix').find_all('a')
        for AV_url in av_urls:
            av_url = 'http://www.xinsss999.com' + AV_url['href']
            self.savefile(av_url)

    def savefile(self, av_url):
        f = open('xinsss.txt', 'a')
        f.write(av_url)
        f.close()






if __name__ == '__main__':
    start_url = 'http://www.xinsss999.com/list/index6.html'
    Spider = XinSpider()
    Spider.all_urls(start_url=start_url)
