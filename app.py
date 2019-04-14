from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from DownloadFunctions import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/download', methods=['GET', 'POST'])
def test():
	temp = {
		'title': request.args['query[track]'], 
		'artist': request.args['query[artist]'], 
		'album': request.args['query[artist]'], 
		'cover': None, 
		'genre': None 
	}
	download()
	return jsonify({"test":1})

if __name__=='__main__':
    app.run(debug=True)