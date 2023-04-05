from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__ , static_folder:= "/static")

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/auction')
def auction():
	return render_template("auction.html")

if __name__ == '__main__':
    app.debug = True
    app.run()