from contents import MyWordcloud
from myDriver import MyDriver
from youtubeCrawler import Crawler
from PIL import Image
import io
import numpy as np

import time

driver = MyDriver()

url = "https://www.youtube.com/results?search_query=AI+Network"

page = driver.page_loader(url=url, num=2)

crawler = Crawler()

yl = crawler.mk_youtuber_list(page)

url = "https://www.youtube.com/channel/UCnyBeZ5iEdlKrAcfNbZ-wog/videos"

page = driver.page_loader(url, 4)

tl = crawler.mk_title_list(page)

print(tl)
print(len(tl))

wc = MyWordcloud(tl)
wc.run()
result = wc.show_word_cloud()

result = io.BytesIO(result)

print(result)
