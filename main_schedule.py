# -*- coding: utf-8 -*-
"""
Created on 2022-03-24 00:40:38
---------
@summary: 爬虫计划任务
---------
@author: abc
"""
import time

from feapder.utils.log import log
from spiders import *

MIN_TASK_COUNT = 1000

if __name__ == "__main__":

    frequency = 300  # every n seconds to assign the tasks
    mins10_timer = 2
    mins20_timer = 4

    i = 0
    while 1:
        """Assign scrape mission to redis every 5 minutes"""

        log.debug('---Pushing Spider1')
        spider = chinanews.Chinanews(redis_key="scraper:spider1", min_task_count=MIN_TASK_COUNT)
        spider.start_monitor_task()
        spider.init_metrics()

        # Scrape every 10min
        if i % mins10_timer == 0:
            # Spider2
            log.debug('---Pushing Spider2')
            spider = spider2.Baidu(redis_key="scraper:spider2", min_task_count=MIN_TASK_COUNT)
            spider.start_monitor_task()
            spider.init_metrics()

        log.info('---Pushing Queue Over, wait for 300s')
        time.sleep(300)

        i += 1
