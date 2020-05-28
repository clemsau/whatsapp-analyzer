import os, uuid
from flask import render_template, request, send_from_directory

from core.utils import parse_file, dataframe_insight
from core.app import app


@app.route('/robots.txt')
@app.route('/sitemap.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template('errors/405.html'), 405


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')


@app.route('/analysis', methods=['POST'])
def analysis():
    if 'file' in request.files:
        file = request.files['file']
        file_name = uuid.uuid4().hex + '.txt'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)    # save file
        try:
            df = parse_file(file_path)  # analysis
            os.remove(file_path)    # remove file
            context = {'analysis': dataframe_insight(df)}
            return render_template('analysis.html', context=context)
        except Exception as e:
            os.remove(file_path)  # remove file
            return render_template('errors/file_processing_error.html')
    else:
        return render_template('errors/file_processing_error.html')


@app.route('/showcase', methods=['GET'])
def showcase():
    try:
        df = parse_file('static/samples/sample_chat.txt')  # analysis
        context = {'analysis': dataframe_insight(df)}
        return render_template('analysis.html', context=context)
    except Exception as e:
        return render_template('errors/file_processing_error.html')
