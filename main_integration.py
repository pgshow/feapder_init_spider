# -*- coding: utf-8 -*-
"""
Created on 2022-03-24 00:40:38
---------
@summary: 爬虫集成
---------
@author: abc
"""
import time

from feapder import Spider
from spiders import *

while True:
    spider = Spider(redis_key="feapder:spider_integration", thread_count=2, delete_keys=True)

    spider.add_parser(chinanews.Chinanews)
    spider.add_parser(spider2.Baidu)

    spider.start()

    time.sleep(600)
