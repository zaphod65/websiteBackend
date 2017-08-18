from flask import Flask, Response, jsonify
import requests
from lxml import html
import json

import LastFmScraper

app = Flask(__name__)
app.debug = True

@app.route('/greet/<name>')
def hello(name):
    greeting = "Hello there, {}!".format(name)
    return Response(json.dumps({'greeting': greeting}), mimetype='application/json')

@app.route('/debug')
def debug():
    return Response(json.dumps(dir(app)), mimetype='application/json')

@app.route('/test')
def test():
    return "This is a test!"

@app.route('/song_list')
def song_list():
    try:
        page = requests.get('https://www.last.fm/user/Zaphodb65')
    except requests.ConnectionError:
        resp = jsonify({'error': 'Could not connect to last.fm'})
        resp.status_code = 500
        return resp
    songs = LastFmScraper.scrape_from_string(page.content)

    return Response(json.dumps(songs), mimetype='application/json')


if __name__ == "__main__":
    app.run()
