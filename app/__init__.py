from flask import Flask, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os.path

app = Flask(__name__, instance_relative_config=True, static_url_path = "", static_folder = "../dist")
app.config.from_pyfile('config.py')
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.api import account, hospital, docor, record, medcard


################################# Static File ####################################
def get_file(filename):
    try:
        src = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('../dist/index.html')
    return Response(content, mimetype="text/html")

@app.errorhandler(404)
def page_not_found(e):
    content = get_file('../dist/index.html')
    return Response(content, mimetype="text/html")