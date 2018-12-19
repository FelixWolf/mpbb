from app import app, render_template
from flask import request

@app.route('/')
def index():
    return render_template("index.htm")

@app.route('/about')
def about():
    return render_template("about.htm")

@app.route('/faq')
def faq():
    return render_template("faq.htm")
