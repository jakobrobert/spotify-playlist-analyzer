from flask import Flask

app = Flask(__name__)


@app.route("/spotify-playlist-analyzer/dev/")
def index():
    return "<p>Hello, World!</p>"
