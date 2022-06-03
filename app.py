from flask import flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)