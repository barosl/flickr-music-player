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


@app.route('/check/')
def check():
	try: cmd = open('cmd.txt').read().strip()
	except: return 'none'

	import os
	try: os.remove('cmd.txt')
	except: pass

	return cmd


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
