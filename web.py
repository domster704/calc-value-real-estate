from flask import render_template, send_from_directory
from app import app

FLUTTER_WEB_APP = 'templates'


@app.route('/')
def render_page():
    return render_template('index.html')


@app.route('/<path:name>')
def return_flutter_doc(name):
    datalist = str(name).split('/')
    DIR_NAME = FLUTTER_WEB_APP

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])
