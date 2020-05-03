from flask import Flask, render_template

import core.conf.settings as settings

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_FOLDER)
app.secret_key = settings.SECRET_KEY


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
