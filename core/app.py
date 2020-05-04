import os
from flask import Flask, render_template, request
import uuid

import core.conf.settings as settings
from .utils import parse_file, create_upload_folder

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_FOLDER)
app.secret_key = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
create_upload_folder()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analysis', methods=['POST'])
def analysis():
    print(request.files)
    if 'file' in request.files:
        file = request.files['file']
        file_name = uuid.uuid4().hex + '.txt'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)    # save file

        df = parse_file(file_path)  # analysis
        os.remove(file_path)    # remove file
        context = {'nb_rows': df.size}
        return render_template('analyse.html', context=context)
    else:
        return 'Issue'
