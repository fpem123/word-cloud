FROM python

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install wordcloud \
    konlpy \
    nltk \
    selenium \
    waitress \
    matplotlib

EXPOSE 80
COPY . .

CMD ["python", "src/app.py"]