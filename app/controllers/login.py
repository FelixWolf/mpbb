from app import app, render_template
from flask import request

@app.route('/login')
def showLogin():
    return render_template("login.htm")

@app.route('/login', methods=['POST'])
def doLogin():
    return render_template("login_sent.htm")
