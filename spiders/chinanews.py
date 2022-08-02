# -*- coding: utf-8 -*-
"""
Created on 2022-08-02 15:14:55
---------
@summary: Requests code demo
---------
@author: abc
"""
import sys
import cn2en
import feapder

from addict import Dict
from feapder.utils.log import log
from items.spider_data import PgSpiderDataItem

SpiderName = 'ChinaNews'


# class Chinanews(feapder.BaseParser): # 如使用爬虫集成模式，则需要继承 BaseParser
class Chinanews(feapder.Spider):
    __custom_setting__ = dict(
        LOG_PATH=f"log/%s.log" % SpiderName,
        PROXY_ENABLE=False,
    )

    def start_requests(self):
        yield feapder.Request("https://www.chinanews.com.cn/scroll-news/news1.html", filter_repeat=False)  # 首页

    def parse(self, request, response):
        try:
            soup = response.bs4()
            # soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.select('.content_list ul>li'):
                if item.has_attr("class"):
                    continue

                data = Dict()

                # Title
                data.title = item.select_one('.dd_bt > a').text

                # Article url
                url = item.select_one('.dd_bt > a').get('href')

                yield feapder.Request(url, callback=self.article_parse, extra=data)

        except Exception as e:
            raise Exception(f'Extraction err: {e}')

    def validate(self, request, response):
        if hasattr(response, 'status_code'):
            if response.status_code != 200:
                raise Exception(f"Fetch {SpiderName} failed, status: {response.status_code}")

    def article_parse(self, request, response):

        news_info = PgSpiderDataItem()
        news_info.table_name = "articles"

        # Set Info
        news_info.chinese_title = request.extra.title

        news_info.url = request.url
        news_info.site = SpiderName

        yield news_info


class Steps:
    """专属步骤"""

    @staticmethod
    def custom_function(params):
        """Custom function"""
        pass


if __name__ == "__main__":
    # from loguru import logger
    # logger.remove()
    # logger.add(sys.stderr, format=cn2en.formatter)

    Chinanews(redis_key=f"scraper:{SpiderName}", auto_start_requests=True, keep_alive=True, thread_count=1).start()

    # # Debug
    # spider = Chinanews.to_DebugSpider(
    #     redis_key=f"scraper:{SpiderName}",
    #     request=feapder.Request(
    #         url="https://www.chinanews.com.cn/life/2022/07-25/9811922.shtml",
    #         callback=Chinanews.article_parse
    #     )
    # )
    # spider.start()