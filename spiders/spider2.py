# -*- coding: utf-8 -*-
"""
Created on 2022-08-02 15:14:55
---------
@summary:
---------
@author: abc
"""
import sys
import cn2en
import feapder

from addict import Dict
from bs4 import BeautifulSoup
from feapder.utils.log import log
from items.spider_data import PgSpiderDataItem
from feapder.network.proxy_pool import ProxyPool

# proxy_pool = ProxyPool(reset_interval_max=300, reset_interval=5, check_valid=True)
# feapder.Request.proxies_pool = proxy_pool

SpiderName = 'Baidu'


class Baidu(feapder.Spider):
    __custom_setting__ = dict(
        # SPIDER_SLEEP_TIME=(
        #     [10, 20]  # Downloading interval seconds. Support random, e.g. SPIDER_SLEEP_TIME = [2, 5] the random will be 2~5 seconds，include 2 and 5
        # ),
        PROXY_EXTRACT_API="",
        PROXY_ENABLE=False,
        # 浏览器渲染
        WEBDRIVER=dict(
            pool_size=1,  # 浏览器的数量
            load_images=False,  # 是否加载图片
            user_agent=None,  # 字符串 或 无参函数，返回值为user_agent
            proxy=None,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
            headless=False,  # 是否为无头浏览器
            driver_type="FIREFOX",  # CHROME 、PHANTOMJS、FIREFOX
            timeout=60,  # 请求超时时间
            window_size=(1920, 1080),  # 窗口大小
            executable_path=None,  # 浏览器路径，默认为默认路径
            render_time=10,  # 渲染时长，即打开网页等待指定时间后再获取源码
            custom_argument=["--ignore-certificate-errors"],  # 自定义浏览器渲染参数
            xhr_url_regexes=None,  # 拦截xhr接口，支持正则，数组类型
            auto_install_driver=True,  # 自动下载浏览器驱动 支持chrome 和 firefox
        )
    )

    def start_requests(self):
        yield feapder.Request("https://www.baidu.com/s?wd=%E6%96%B0%E9%97%BB", render=True, filter_repeat=False)

    def parse(self, request, response):
        try:
            soup = response.bs4()
            # soup = BeautifulSoup(response.text, 'html.parser')

            for article in soup.select('h3 > a'):
                title = article.text
                log.debug(title)
                yield feapder.Request(article.get('href'), callback=self.article_parse, render=True, filter_repeat=True)

        except Exception as e:
            raise Exception(f'Extraction err: {e}')

    def article_parse(self, request, response):
        try:
            title = response.xpath('//title/text()').extract_first()
            log.info(title)

        except Exception as e:
            raise Exception(f'Extraction err: {e}')


if __name__ == "__main__":
    Baidu(redis_key=f"scraper:{SpiderName}", auto_start_requests=True, keep_alive=True, thread_count=1, delete_keys=True).start()

    # # Debug
    # spider = Baidu.to_DebugSpider(
    #     redis_key=f"scraper:{SpiderName}",
    #     request=feapder.Request(
    #         url="https://baijiahao.baidu.com/s?id=1739712336071253570&wfr=spider&for=pc",
    #         callback=Baidu.article_parse,
    #         render=True,
    #     ),
    # )
    # spider.start()
