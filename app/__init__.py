from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.api import account, hospital, docor, record, medcard



