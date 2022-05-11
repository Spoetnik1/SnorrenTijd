from flask import Flask
from snorrenapp.loggingutils import configure_logger
import configparser


configure_logger()

configuration = 'DEFAULT'

config = configparser.ConfigParser()
config.read('config.ini')

# logging.basicConfig(filename='snorrenTijdWebServer.log', level=logging.INFO)

app = Flask(__name__)

app.config['SECRET_KEY'] = config[configuration]['secret_key']
app.config["IMAGE_UPLOADS"] = config[configuration]['image_file_path']
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# import routes after the app is initialised, because the routes uses the app, therefore the app must
# initialised first.
from snorrenapp import routes