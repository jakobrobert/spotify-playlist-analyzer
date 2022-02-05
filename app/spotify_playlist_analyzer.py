from flask import Flask

import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return "<p>Hello, World!</p>"
