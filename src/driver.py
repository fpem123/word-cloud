'''
    Name: contents.py
    Writer: Hoseop Lee, Ainizer
    Rule: make YouTuber's video title list
'''

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
import time


'''
    Name: Driver()
    Writer: Hoseop Lee, Ainizer
    Des: 크롤러 클래스 
'''
class Driver():
    _driver: webdriver

    def __init__(self):
        # selenium options
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self._driver = webdriver.Chrome('chromedriver', chrome_options=options)
        self._driver.implicitly_wait(1)

    def search_page_loader(self, url, num):
        self._driver.get(url)

        body = self._driver.find_element_by_tag_name('body')

        for count in range(num):
            last = self._driver.execute_script('return document.documentElement.scrollHeight')

            for i in range(num):
                body.send_keys(Keys.END)
                time.sleep(0.5)

            current = self._driver.execute_script('return document.documentElement.scrollHeight')

            if last == current:
                break

        page = self._driver.page_source

        return page

    # 자원 정리를 위한 세르니움 종료 메소드
    def quit_driver(self):
        self._driver.quit()
