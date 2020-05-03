import os
import core.conf.secret_settings as secrets

SECRET_KEY = secrets.SECRET_KEY

BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATE_FOLDER = os.path.join(BASE_FOLDER, 'templates/')
STATIC_FOLDER = os.path.join(BASE_FOLDER, 'static/')
