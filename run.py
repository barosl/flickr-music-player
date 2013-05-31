from flask import Flask, render_template
app = Flask(__name__)

from flask import request
import urllib


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/proxy/')
def proxy():
    url = request.args.get('url')
    return urllib.urlopen(url).read()


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
