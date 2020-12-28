'''
    Name: youtuberCrawler.py
    Writer: Hoseop Lee, Ainizer
    Rule: make YouTuber's video title list
    update: 20.12.28
'''
from bs4 import BeautifulSoup

'''
    Name: Crwler()
    Writer: Hoseop Lee, Ainizer
    Des: 크롤러 클래스 
'''
class Crawler():

    def __init__(self):
        self.korean = False          # is Korean

    # 유튜버 채널을 크롤링하여 리스트로 만드는 메소드
    def mk_youtuber_list(self, page):
        soup = BeautifulSoup(page, 'lxml')
        youtubers = soup.find_all(id='info-section')

        result = dict()

        for youtuber in youtubers:
            anchor = youtuber.find('a')
            name = youtuber.find(id='tooltip').string.strip()
            result[name] = anchor.get('href')

        return result

    # 유튜버 영상들의 제목을 크롤링하여 리스트로 만드는 메소드
    def mk_title_list(self, page):
        soup = BeautifulSoup(page, 'lxml')
        videos = soup.find_all(id='dismissable')

        titles = []

        for video in videos:
            title = video.find(id='video-title')

            if len(title.text.strip()) > 0:
                titles.append(title.text)

        return titles
