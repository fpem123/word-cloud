'''
    Name: app.py
    Writer: Hoseop Lee, Ainizer
    Rule: Flask app
    update: 20.12.29
'''

# external module
from flask import Flask, request, Response, jsonify, send_file, render_template, current_app
from PIL import Image

# internal module
from queue import Queue, Empty
import io
import os
import time
import threading

# my module
from youtubeCrawler import Crawler
from myDriver import MyDriver
from contents import MyWordcloud

driver = MyDriver()
wc = MyWordcloud()

requests_queue = Queue()
BATCH_SIZE = 1          # also max queue size
CHECK_INTERVAL = 0.1
RESULT_FOLDER = 'img_data'

app = Flask(__name__)

# request handler
def handle_requests_by_batch():
    try:
        while True:
            requests_batch = []

            while not (len(requests_batch) >= BATCH_SIZE):
                try:
                    requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
                except Empty:
                    continue

            for requests in requests_batch:
                if len(requests["input"]) == 1:
                    requests['output'] = run_crawl(requests['input'][0])
                elif len(requests["input"]) == 2:
                    requests['output'] = run_wordcloud(requests['input'][0])

    except Exception as e:
        while not requests_queue.empty():
            requests_queue.get()
        print(e)


threading.Thread(target=handle_requests_by_batch).start()


# find target youtuber
def run_crawl(target):
    url = f'https://www.youtube.com/results?search_query={target}'

    page = driver.page_loader(url, 2)
    crawler = Crawler()

    youtubers = crawler.mk_youtuber_list(page)

    result = {}

    for idx, youtuber in enumerate(youtubers):
        result[idx] = youtuber

    if len(result) == 0:
        return jsonify({'message': 'Youtuber not found, try again'}), 404

    return 'crawl', result


# make word cloud
def run_wordcloud(target):
    try:
        # bocking user mistake
        if target[0] != '/':
            target = '/' + target

        url = f'https://www.youtube.com{target}/videos'

        page = driver.page_loader(url, 5)
        crawler = Crawler()

        titles = crawler.mk_title_list(page)

    except Exception:
        return jsonify({'message': 'Crawler error'}), 400

    if len(titles) == 0:
        return jsonify({'message': 'No videos'}), 400

    # make word cloud part
    try:
        wc.set_text(titles)
        wc.run()

        result = wc.show_word_cloud()

        target = target.split(sep='/')[1]

        # make dir
        os.makedirs(RESULT_FOLDER, exist_ok=True)
        path = os.path.join(RESULT_FOLDER, target)

        # save result image. If not save image, you will see missing image.
        Image.fromarray(result).save(path, 'jpeg')

        with open(path, 'rb') as f:
            data = f.read()
        result = io.BytesIO(data)

        os.remove(path)

        return 'wc', result

    except Exception:
        return jsonify({'message': 'Word cloud error'}), 400


@app.route('/queue-clear')
def queue_debug():
    try:
        requests_queue.queue.clear()

        return 'Clear', 200
    except Exception:
        return jsonify({'message': 'Queue clear error'}), 400


@app.route('/word-cloud/<types>', methods=['POST'])
def generation(types):
    try:
        if requests_queue.qsize() > BATCH_SIZE:
            return jsonify({'message': 'Error! Too many request'}), 429

        try:
            args = []

            if types == 'find_youtuber':
                target = str(request.form['youtuber'])
                args.append(target)
            elif types == 'make_wordcloud':
                target = str(request.form['youtube_url'])
                args.append(target)
            else:
                return jsonify({'message': 'Error! Wrong type'}), 400

            # Add type identify
            if types == 'make_wordcloud':
                args.append(True)

        except Exception:
            return jsonify({'message': 'Error! Wrong request'}), 500

        req = {'input': args}
        requests_queue.put(req)

        while 'output' not in req:
            time.sleep(CHECK_INTERVAL)

        result = req['output']

        if result[0] == 'crawl':
            return result[1]
        # word cloud result is a image. so, need send_file method. This is important.
        elif result[0] == 'wc':
            return send_file(result[1], mimetype='image/jpeg'), 200

    except Exception:
        return jsonify({'message': 'Error! Unable'}), 400


@app.route('/healthz')
def health():
    return "Health", 200


@app.route('/')
def main():
    return render_template('main.html'), 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')