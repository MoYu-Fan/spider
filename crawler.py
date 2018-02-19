# -*-coding:utf-8-*-
# coding: utf-8
# coding: gb2312
# __author__='admin'

import urlparse
import itertools
from download import Downloader
import re

D = Downloader()


class Crawler(object):

    def ID_crawler(self, start_url, max_depth=15, max_errors=3):
        global html
        depth = 1
        num_errors = 0
        for page in itertools:
            page_url = start_url + '/%d.html' % page
            if depth != max_depth:
                depth = depth + 1
                html = D(page_url).text
                if html is None:
                    num_errors = num_errors + 1
                    if num_errors == max_errors:
                        print 'It is full of Errors.'
                        break
                else:
                    num_errors = 0
            else:
                break

        return html

    def link_crawler(self, start_url, link_regex, max_depth=-1):
        crawl_queue = [start_url]
        seen = {}
        while crawl_queue:
            url = crawl_queue.pop()
            html = D(url)
            depth = seen[url]
            if depth != max_depth:
                for link in self.get_links(html):
                    if re.match(link_regex, link):
                        link = urlparse.urljoin(start_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)

    def get_links(self, html):
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        return webpage_regex.findall(html)
