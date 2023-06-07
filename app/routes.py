from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extraction')
def extraction():
    return render_template("extraction.html")

@app.route('/list')
def list():
    return render_template("list.html")

@app.route('/productsite')
def productsite():
    return render_template("productsite.html")

@app.route('/charts')
def charts():
    return render_template("charts.html")

@app.route('/author')
def author():
    return render_template("author.html")