from flask import Flask

import configparser

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]

app = Flask(__name__)

@app.route(URL_PREFIX + "hello-world", methods=["GET"])
def index():
    return "<h1>Hello World!<h1>"
