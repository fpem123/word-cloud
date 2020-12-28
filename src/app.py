'''
    Name: app.py
    Writer: Hoseop Lee, Ainizer
    Rule: Flask app
    update: 20.12.28
'''
from flask import Flask, request, Response, jsonify
from youtubeCrawler import Crawler
from myDriver import MyDriver
from contents import MyWordcloud

from queue import Queue, Empty
import time
import threading

app = Flask(__name__)

driver = MyDriver()

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1


def handle_requests_by_batch():
    while True:
        requests_batch = []

        while not (len(requests_batch) >= BATCH_SIZE):
            try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

        batch_output = []

        for requests in requests_batch:
            if len(requests["input"]) == 1:
                requests['output'] = run_crawl(requests['input'][0])
            elif len(requests["input"]) == 2:
                requests['output'] = run_wordcloud(requests['input'][0])


threading.Thread(target=handle_requests_by_batch).start()


def run_crawl(target):
    url = f'https://www.youtube.com/results?search_query={target}'

    page = driver.search_page_loader(url, 2)
    crawler = Crawler()

    youtubers = crawler.mk_youtuber_list(page)

    result = {}

    for idx, youtuber in enumerate(youtubers):
        result[idx] = youtuber

    if len(result) == 0:
        return jsonify({'message': 'Youtuber not found, try again'}), 404

    return result


def run_wordcloud(target):
    try:
        url = f'https://www.youtube.com/{target}/videos'

        page = driver.search_page_loader(url, 4)
        crawler = Crawler()

        titles = crawler.mk_title_list(page)
    except Exception:
        return jsonify({'message': 'Crawler error'}), 400

    if len(titles) == 0:
        return jsonify({'message': 'No videos'}), 400

    try:
        wc = MyWordcloud(titles)
        wc.run()

        result = wc.show_word_cloud()

        return result
    except Exception:
        return jsonify({'message': 'Word cloud error'}), 400


@app.route('/word-cloud/<types>', methods=['POST'])
def generation(types):
    try:
        if types != 'find_youtuber' and types != 'find_video':
            return jsonify({'message': 'Error! Wrong type'}), 400
        if requests_queue.qsize() > BATCH_SIZE:
            return jsonify({'message': 'Error! Too many request'}), 429

        try:
            args = []

            target = str(request.form['youtuber'])

            args.append(target)

            if types == 'find_video':
                args.append(True)

        except Exception:
            return jsonify({'message': 'Error! Wrong request'}), 500

        req = {'input': args}
        requests_queue.put(req)

        while 'output' not in req:
            time.sleep(CHECK_INTERVAL)

        result_image = req['output']

        return result_image

    except Exception:
        return jsonify({'message': 'Error! Unable'}), 400


@app.route('/healthz')
def health():
    return "Health", 200


@app.route('/')
def main():
    return "Ok", 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')