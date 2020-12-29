from contents import MyWordcloud
from myDriver import MyDriver
from youtubeCrawler import Crawler
from PIL import Image
import io
import os

RESULT_FOLDER = 'img_data/'

driver = MyDriver()

url = "https://www.youtube.com/results?search_query=AI+Network"

page = driver.page_loader(url=url, num=2)

crawler = Crawler()

yl = crawler.mk_youtuber_list(page)

print(yl)

url = "https://www.youtube.com/channel/UCnyBeZ5iEdlKrAcfNbZ-wog/videos"

page = driver.page_loader(url, 4)

tl = crawler.mk_title_list(page)

print(tl)
print(len(tl))

wc = MyWordcloud(tl)
wc.run()
result = wc.show_word_cloud()


os.makedirs(RESULT_FOLDER, exist_ok=True)
path = os.path.join(RESULT_FOLDER, 'wc')

Image.fromarray(result).save(path, 'jpeg')

with open(path, 'rb') as f:
    data = f.read()
result = io.BytesIO(data)

driver.quit_driver()

print(result)
