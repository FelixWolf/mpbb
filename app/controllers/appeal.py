from app import app, render_template
from flask import request

@app.route('/appeal')
def showAppeal():
    return render_template("appeal.htm")

@app.route('/appeal', methods=['POST'])
def doAppeal():
    return render_template("appeal.htm")
