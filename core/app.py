from flask import Flask

import core.conf.settings as settings
from core.utils import create_upload_folder

app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER, static_folder=settings.STATIC_FOLDER)
app.secret_key = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER

# Create an upload folder if it not exist yet
create_upload_folder()
