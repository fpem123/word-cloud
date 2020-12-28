FROM python

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install wordcloud \
    konlpy \
    nltk \
    selenium \
    waitress

EXPOSE 80
COPY . .

RUN cd src

CMD ["python", "app.py"]