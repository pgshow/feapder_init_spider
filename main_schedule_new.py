# -*- coding: utf-8 -*-
"""
Created on 2022-03-24 00:40:38
---------
@summary: 爬虫计划任务
---------
@author: abc
"""
import importlib
import time
import inspect
import spiders

from feapder.utils.log import log

MIN_TASK_COUNT = 1000


def get_classobj(file_name):
    """Get class object by python file name"""
    module_object = importlib.import_module(f"spiders.{file_name}")
    cls_members = inspect.getmembers(module_object)

    SpiderName = ''
    ClassObj = None

    # Get spider class name and SpiderName
    for name, obj in cls_members:
        if name == 'SpiderName':
            SpiderName = obj
        if hasattr(obj, "start_requests"):
            ClassObj = obj

    return SpiderName, ClassObj


if __name__ == "__main__":
    spider_libs = spiders.__all__  # 可以批量分配 spiders.__all__ 里未被注释模块的任务

    while 1:
        """Assign scrape mission to redis every 1 hour"""

        for lib_name in spider_libs:
            log.debug(f'---Pushing {lib_name}')
            SpiderName, SpiderCls = get_classobj(lib_name)
            spider = SpiderCls(redis_key=f"scraper:{SpiderName}", min_task_count=MIN_TASK_COUNT)
            spider.start_monitor_task()
            spider.init_metrics()

        log.info('---Pushing Queue Over, wait for next hour')
        time.sleep(3600)
