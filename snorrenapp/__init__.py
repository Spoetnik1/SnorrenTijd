from flask import Flask, session
import os
import flask_sijax
#from flask_session import Session


app = Flask(__name__)

app.config['SECRET_KEY'] = '4255f9af8f7cb026d315ac0c8aeda159'
app.config["IMAGE_UPLOADS"] = 'C:/Users/super/IdeaProjects/snorren/snorrenapp/static/uploaded_images/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# The path where you want the extension to create the needed javascript files
# DON'T put any of your files in this directory, because they'll be deleted!
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')

# You need to point Sijax to the json2.js library if you want to support
# browsers that don't support JSON natively (like IE <= 7)
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

from snorrenapp import routes