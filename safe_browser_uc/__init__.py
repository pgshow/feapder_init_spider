import json
import random
import re
import os
import signal
import time
import psutil
import requests

import undetected_chromedriver as uc

from carehttp import Carehttp
from undetected_chromedriver.options import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from safe_browser_uc import profile, bypass, folder_control
from webdriver_manager.core.utils import get_browser_version_from_os


def get_one_proxy(api_url):
    try:
        r = Carehttp(mark='Proxy Api', tries=3, delay=2).get(api_url, timeout=20)
        if r.status_code != 200:
            raise Exception(f"Status {r.status_code}")

        if not re.search(r'\d{1,3}:\d{2,5}', r.text):
            raise Exception(f"Invalid Api response")

        return r.text
    except Exception as e:
        raise Exception(f"Get Proxy err: {e}")


def get_options(headless=False, css=False, images=False, js=False):
    """
    Get Chrome options
    :param headless: bool True for headless mode
    :param images: bool False for images disabled
    :param js: bool False for javascript disabled
    :return:
    """
    options = ChromeOptions()

    if headless:
        driver_options.add_argument("--headless")

    prefs = {
        'profile.default_content_settings.popups': 0,
        'profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player': 1,  # disable play video automatically
        'profile.default_content_setting_values': {}
    }

    if not css:
        _add_extension(options, 'CSS-Block-1.0.0_0')  # disable css

    if not images:
        prefs['profile.default_content_setting_values']['images'] = 2  # disable images

    if not js:
        prefs['profile.default_content_setting_values']['javascript'] = 2  # disable js

    options.add_experimental_option("prefs", prefs)

    # Set a tmp folder for User Data of Chrome
    path = folder_control.make_chrome_tmp_folder()
    # path = 'C:\\Users\\admin\\PycharmProjects\\feapder_init_spider\\safe_browser_uc\\Chrome\\UserData - 用来设置'
    options.add_argument(f"--user-data-dir={path}")

    return options


def _add_extension(options, extension_name):
    """Add extension to Chrome"""
    extension_root = os.path.dirname(__file__)
    extension_path = f'{extension_root}/{extension_name}'

    paths_list = [extension_path]

    # If there already has extensions
    if len(options.arguments) > 0:
        for arg in options.arguments:
            if arg.startswith('--disable-extensions-except='):
                paths_str = re.search(r'--disable-extensions-except=(.+)$', arg).group(1)
                paths_list = paths_list + paths_str.split(',')  # get exist paths
                options.arguments.remove(arg)  # remove old paths from arguments

        for arg in options.arguments:
            if arg.startswith('--load-extension='):
                options.arguments.remove(arg)  # remove old paths from arguments

    # Add extension to Options
    options.add_argument(f'--disable-extensions-except={",".join(paths_list)}')
    options.add_argument(f'--load-extension={",".join(paths_list)}')


class SafeDriver:
    def __init__(self, options, proxy=None, proxy_type='https'):
        """
        Initialize the browser driver with proxy or without proxy
        :param proxy: str IP:port
        :param proxy_type: str https or socks5
        """
        self.options = options

        try:
            if proxy:
                # use driver with proxy
                if proxy_type == 'https':
                    self.driver = self.chrome_init(http_proxy=proxy)
                elif proxy_type == 'socks5':
                    self.driver = self.chrome_init(socks5_proxy=proxy)
            else:
                # use driver without proxy
                self.driver = self.chrome_init()

        except Exception as e:
            raise Exception(f'SafeDriver err: {e}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.__kill()

    def __kill(self):
        """Kill the browser to avoid zombie process"""
        # get the PIDs
        self.driver.service.process
        p = psutil.Process(self.driver.service.process.pid)
        children = p.children(recursive=True)

        # quite selenium
        self.driver.quit()

        # kill the chrome PIDs
        for child in children:
            try:
                # kill child pid
                os.kill(child.pid, signal.SIGKILL)
            except:
                pass
        try:
            # kill main pid
            os.kill(p.pid, signal.SIGKILL)
        except:
            pass
        time.sleep(1)

    def chrome_init(self, socks5_proxy=None, http_proxy=None):
        """Initialize Chrome driver"""
        _add_extension(self.options, 'WebRTC-Leak-Prevent-1.0.14')
        _add_extension(self.options, 'spoof-timezone')
        _add_extension(self.options, 'URL-Blocker-0.911_0')

        if socks5_proxy:
            self.options.add_argument(f"--proxy-server=socks5://{socks5_proxy}")
        elif http_proxy:
            self.options.add_argument(f"--proxy-server={http_proxy}")

        driver = uc.Chrome(options=self.options, version_main=self._get_driver_version())
        time.sleep(2)

        try:
            # Set timezone
            self._set_timezone(driver, 1)  # set proxy timezone for browser

            # Choose the option to disable webRTC
            # self._disable_webrtc(driver, 2)

            size = random.choice(profile.chrome_size)
            driver.set_window_size(size[0], size[1])
            return driver
        except Exception as e:
            if self.driver:
                self.__kill()
            raise e

    def _disable_webrtc(self, driver, extension_index):
        """disable webRTC, so cloudflare can't get real ip by it"""
        # Find spoof-timezone extension id
        driver.get('chrome://extensions/')
        time.sleep(1)
        extension_id = driver.execute_script(
            f'return document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelector("extensions-item:nth-child({extension_index})").getAttribute("id")')

        driver.get(f'chrome-extension://{extension_id}/html/options.html')
        time.sleep(1)
        s = Select(driver.find_element(By.CSS_SELECTOR, 'select#policy'))
        s.select_by_value('disable_non_proxied_udp')

    def _set_timezone(self, driver, extension_index):
        """Set timezone, latitude and longitude"""
        timezone_json = self.__get_timezone(driver)  # get timezone of proxy

        # Find spoof-timezone extension id
        driver.get('chrome://extensions/')
        time.sleep(1)

        # 获取插件ID, 若你想在控制台测试该代码, 先去掉 return 才能正确运行
        extension_id = driver.execute_script(
            '''var extension_name = "Spoof Timezone";
            var extension_id = "";
            var items = document.querySelector("body > extensions-manager").shadowRoot.querySelector("#items-list").shadowRoot.querySelectorAll("extensions-item"), i;
            for (i = 0; i < items.length; ++i) {
            head = items[i].shadowRoot.querySelector("#name-and-version > #name").textContent
            if (head == extension_name) {
            console.log(items[i].getAttribute("id"));
            extension_id = items[i].getAttribute("id");
            break;
            }
            }
            return extension_id;'''
        )

        # Open timezone plugin panel
        extension_url = f'chrome-extension://{extension_id}/data/options/index.html'
        driver.get(extension_url)
        time.sleep(1)

        # Choose target timezone and save
        select = Select(driver.find_element(By.CSS_SELECTOR, "select#offset"))
        if timezone_json['timezone'] in driver.page_source:
            select.select_by_value(timezone_json['timezone'])  # Timezone name is in the input list, choose it
        else:
            driver.find_element(By.CSS_SELECTOR, 'input#random').click()  # There has no this Timezone name, so choose random timezone option

        try:
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'input[value="Save"]').click()
        except:
            pass

    @staticmethod
    def __get_timezone(driver):
        """Get timezone, latitude and longitude"""
        driver.get('https://api.ipgeolocation.io/timezone?apiKey=997cfe918ac8479ca53e52da2d00b9f3')
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//pre[contains(text(), timezone)]')))

            code = driver.find_element(By.CSS_SELECTOR, 'body > pre').get_attribute('innerHTML')

            json_date = json.loads(code)

            return json_date
        except Exception as e:
            raise Exception(f"Get Timezone err: {e}")

    def _get_driver_version(self):
        """Use webdriver_manager to Get Chrome driver version"""
        try:
            driver_last_version = get_browser_version_from_os('google-chrome')
            driver_version = int(driver_last_version.split('.')[0])

            return driver_version
        except:
            raise Exception('Get Driver version failed')


if __name__ == '__main__':
    one_proxy = get_one_proxy(
        api_url="http://list.rola.info:8088/user_get_ip_list?token=ig2Nt9VoTq18b7HL1629360050648&type=datacenter&qty=1&time=5&country=&format=txt&protocol=socks5&filter=1")

    driver_options = get_options(images=False, css=True, js=True)

    # 判断操作系统，添加必要的设置

    # with SafeDriver(options=driver_options, proxy=one_proxy, proxy_type='socks5') as chrome:
    with SafeDriver(options=driver_options) as chrome:
        # driver = bypass.prepare_cloudflare('https://www.hermes.com/hk/en/')
        # time.sleep(2)
        driver = chrome.driver
        driver.get('https://www.400zi.com/')
        time.sleep(1000)
