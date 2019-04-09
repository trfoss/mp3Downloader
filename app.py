from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/download')
def test():
	return jsonify({"test":1})

	


if __name__=='__main__':
    app.run(debug=True)