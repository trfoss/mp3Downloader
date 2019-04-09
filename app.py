from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/test')
def test():
	return "Hello from test"


if __name__=='__main__':
    app.run()