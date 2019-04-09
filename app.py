from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from DownloadFunctions import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/download', methods=['GET'])
def test():
	# need to test for empty queries
	# print("QUERIES:",request.args.getlist('queries[]'))
	download(request.args.getlist('queries[]'))
	return jsonify({"test":1})

if __name__=='__main__':
    app.run(debug=True)