from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def prepare_cloudflare(driver, url):
    """Check status if this site protects by cloudflare"""
    if not url.startswith('http'):
        raise Exception('URL must start with protocol')

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//title[contains(text(), 'Just a moment...')]")))

        WebDriverWait(driver, 60).until_not(
            EC.presence_of_element_located(
                (By.XPATH, "//title[contains(text(), 'Just a moment...')]")))

        return driver
    except:
        if "This site can’t be reached" in driver.page_source:
            raise Exception("Chrome fetch failed")
        else:
            raise Exception("Can't bypass cloudflare")

