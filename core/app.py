import os, uuid, logging, time
from flask import Flask, render_template, request, send_from_directory

import core.conf.settings as settings
from .utils import parse_file, create_upload_folder, dataframe_insight

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_FOLDER)
app.secret_key = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

# Create an upload folder if it not exist yet
create_upload_folder()

# Create Logger
logging.basicConfig(filename='logger.log', level=logging.DEBUG)
logger = logging.getLogger()


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
        logger.info("File [{0}] - Received".format(file_name))
        time_before_saving = time.time()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)    # save file
        time_after_saving = time.time()
        logger.info("File [{0}] - Saved, took {1}s".format(file_name, (time_after_saving - time_before_saving)))
        with open(file_path, 'r', encoding='utf-8') as f:  # Log infos about the file
            try:
                logger.info("File [{0}] - line format: {1}".format(file_name, f.readline(0)))
            except:
                logger.error("File [{0}] - Something went wrong, Couldn't access first line".format(file_name))

        try:
            time_before_analysis = time.time()
            logger.info("File [{0}] - Starting parsing".format(file_name))
            df = parse_file(file_path)  # analysis
            logger.info("File [{0}] - Removing file".format(file_name))
            os.remove(file_path)    # remove file
            logger.info("File [{0}] - Starting analysis".format(file_name))
            context = {'analysis': dataframe_insight(df)}
            logger.info("File [{0}] - Rendering template".format(file_name))
            time_after_analysis = time.time()
            logger.info("File [{0}] - Process took {1}s".format(file_name, (time_after_analysis-time_before_analysis)))
            return render_template('analysis.html', context=context)
        except Exception as e:
            logger.error('File [{0}] - Issue encountered: {1}'.format(file_name, str(e)))
            logger.info("File [{0}] - Removing file".format(file_name))
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
        logger.error('Showcase file - Issue encountered: {0}'.format(str(e)))
        return 'Something went wrong with the file'
