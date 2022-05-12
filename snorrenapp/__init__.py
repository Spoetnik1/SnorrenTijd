from flask import Flask
from snorrenapp.loggingutils import configure_logger
import configparser


configuration = 'DEFAULT'
config = configparser.ConfigParser()
config.read('config.ini')

configure_logger(log_level=config[configuration]['logging_level'],
                 logging_filename=config[configuration]['logging_file_name'])

app = Flask(__name__)
app.config['SECRET_KEY'] = config[configuration]['secret_key']
app.config["IMAGE_UPLOADS"] = config[configuration]['image_file_path']
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# import routes after the app is initialised, because the routes uses the app, therefore the app must
# initialised first.
from snorrenapp import routes