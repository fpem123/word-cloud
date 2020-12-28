from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.youtubeCrawler import Crawler
from src.driver import Driver
from src.contents import MyWordcloud

from queue import Queue, Empty
import time
import threading

app = Flask(__name__)

driver = Driver()

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
    url = f'https://www.youtube.com/user/{target}/videos'

    page = driver.search_page_loader(url, 5)
    crawler = Crawler()

    titles = crawler.mk_title_list(page)

    wc = MyWordcloud(titles)
    wc.run()

    result = wc.show_word_cloud()

    return result


@app.route('/wordcloud/<types>', method=['POST'])
def generation(types):
    try:
        if types != 'find_youtuber' or types != 'find_video':
            return jsonify({'message': 'Error!, wrong type'}), 400
        if requests_queue.qsize() > BATCH_SIZE:
            return jsonify({'message': 'Error! Too many request'}), 429

        try:
            args = []

            target = str(request.form['youtuber'])

            args.append(target)
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