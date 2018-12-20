from app import app, render_template
from flask import request

@app.route('/report')
def showReport():
    return render_template("report.htm")

@app.route('/login', methods=['POST'])
def doReport():
    return render_template("login_sent.htm")
