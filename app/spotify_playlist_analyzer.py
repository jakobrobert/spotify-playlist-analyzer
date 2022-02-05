from flask import Flask
from flask import render_template

import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")
