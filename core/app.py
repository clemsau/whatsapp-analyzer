import os
from flask import Flask, render_template, request
import uuid

import core.conf.settings as settings
from .utils import parse_file, create_upload_folder, dataframe_insight

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_FOLDER)
app.secret_key = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
create_upload_folder()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analysis', methods=['POST'])
def analysis():
    if 'file' in request.files:
        file = request.files['file']
        file_name = uuid.uuid4().hex + '.txt'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)    # save file

        df = parse_file(file_path)  # analysis
        os.remove(file_path)    # remove file
        context = {'analysis': dataframe_insight(df)}
        print(context['analysis']['total_word_count'])
        return render_template('analysis.html', context=context)
    else:
        return 'Issue'
