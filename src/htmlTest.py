from flask import Flask, request, Response, jsonify, send_file, render_template, redirect
import io
import os
import time
from PIL import Image

from contents import MyWordcloud

app = Flask(__name__)

RESULT_FOLDER = 'img_data'

wc = MyWordcloud()


@app.route('/word-cloud/make_wordcloud', methods=['POST'])
def send_img():
    text = ['hi', 'hello', 'hi']
    wc.set_text(text)
    wc.run()
    result = wc.show_word_cloud()

    target = request.form['youtube_url']
    target = target.split(sep='/')[1]

    print(target)
    os.makedirs(RESULT_FOLDER, exist_ok=True)

    path = os.path.join(RESULT_FOLDER, target)
    Image.fromarray(result).save(path, 'jpeg')

    time.sleep(2)

    with open(path, 'rb') as f:
        data = f.read()
    result = io.BytesIO(data)

    os.remove(path)

    return send_file(result, mimetype='image/jpeg'), 200


@app.route('/word-cloud/find_youtuber', methods=['POST'])
def send_data():
    print(request.form['youtuber'])

    time.sleep(2)

    return jsonify({'0': ['youtuber1', 'url/iswc'], '1': ['youtuber2', 'url/iswc']}), 200


@app.route('/')
def main(req=None):
    return render_template('main.html'), 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')