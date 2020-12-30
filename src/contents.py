'''
    Name: contents.py
    Writer: Hoseop Lee, Ainizer
    Rule: make word cloud module
    update: 20.12.29
'''
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
from konlpy.tag import Kkma
import nltk


'''
    Name: MyWordcloud()
    Writer: Hoseop Lee, Ainizer
    Des: 워드클라우드 클래스 
'''
class MyWordcloud():
    def __init__(self):
        self.text = None
        self.mask = None
        self.color = 'white'        # default color is white
        self.wordcloud = None
        self.korean = False

    def set_text(self, text):
        self.text = text

    def run(self):
        font = "8CWdFZ7DPDGqlF9o7-ot4M-VDac.ttf"

        target = ' '.join(self.text)

        # Make word cloud object
        wc = WordCloud(font_path=font, max_font_size=40, min_font_size=10,
                       background_color=self.color, mask=self.mask)
    
        self.wordcloud = wc.generate(target)

    # 한국어 워드클라우드를 만드는 메소드
    def _mk_word_cloud_korean(self):
        target = ' '.join(self.text)

        kkma = Kkma()
        n = kkma.nouns(target)

        n = [temp for temp in n if len(temp) != 1 if not temp.isdecimal()]

        text = nltk.Text(n)
        data = text.vocab()
        data500 = data.most_common(500)

        dic = dict(data500)

        # Make word cloud object
        wc = WordCloud(font_path='/Library/Fonts/Arial Unicode.ttf', max_font_size=80, min_font_size=10,
                       background_color=self.color, mask=self.mask)

        self.wordcloud = wc.generate_from_frequencies(dic)

    def set_mask(self, image):
        img = Image.open('images/shape.png')
        self.mask = np.array(img)

    def set_color(self, color):
        self.color = color

    def show_word_cloud(self):
        # convert img to array
        result = WordCloud.to_array(self.wordcloud)

        self.__init__()

        return result
