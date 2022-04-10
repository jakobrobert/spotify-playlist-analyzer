import base64

from flask import Flask, render_template, request, redirect, url_for

import configparser
import operator
import matplotlib.pyplot as plt
from io import BytesIO

from spotify.spotify_client import SpotifyClient

config = configparser.ConfigParser()
config.read("../server.ini")
URL_PREFIX = config["DEFAULT"]["URL_PREFIX"]
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]

spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

app = Flask(__name__)


@app.route(URL_PREFIX, methods=["GET"])
def index():
    return render_template("index.html")


@app.route(URL_PREFIX + "playlist-by-url", methods=["GET"])
def get_playlist_by_url():
    playlist_url = request.args.get("playlist_url")

    playlist_id = __get_playlist_id_from_playlist_url(playlist_url)
    redirect_url = url_for("get_playlist_by_id",
                           playlist_id=playlist_id, sort_by="none", order="ascending")

    return redirect(redirect_url)


@app.route(URL_PREFIX + "playlist/<playlist_id>", methods=["GET"])
def get_playlist_by_id(playlist_id):
    sort_by = request.args.get("sort_by")
    order = request.args.get("order")

    playlist = spotify_client.get_playlist_by_id(playlist_id)
    __sort_tracks(playlist.tracks, sort_by, order)

    return render_template("playlist.html", playlist=playlist, sort_by=sort_by, order=order)


@app.route(URL_PREFIX + "playlist/<playlist_id>/year-distribution", methods=["GET"])
def get_year_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    year_interval_to_percentage = playlist.get_year_interval_to_percentage()
    histogram_image_base64 = __get_year_distribution_histogram_image_base64(year_interval_to_percentage)

    return render_template("year_distribution.html", playlist=playlist,
                           year_interval_to_percentage=year_interval_to_percentage,
                           histogram_image_base64=histogram_image_base64)


@app.route(URL_PREFIX + "playlist/<playlist_id>/tempo-distribution", methods=["GET"])
def get_tempo_distribution_of_playlist(playlist_id):
    playlist = spotify_client.get_playlist_by_id(playlist_id)

    tempo_interval_to_percentage = playlist.get_tempo_interval_to_percentage()
    histogram_image_base64 = __get_tempo_distribution_histogram_image_base64(tempo_interval_to_percentage)

    return render_template("tempo_distribution.html", playlist=playlist,
                           tempo_interval_to_percentage=tempo_interval_to_percentage,
                           histogram_image_base64=histogram_image_base64)


def __get_playlist_id_from_playlist_url(playlist_url):
    start_index = playlist_url.find("playlist/") + len("playlist/")
    end_index = playlist_url.find("?")

    return playlist_url[start_index:end_index]


def __sort_tracks(tracks, sort_by, order):
    if sort_by == "none":
        return

    reverse = (order == "descending")
    tracks.sort(key=operator.attrgetter(sort_by), reverse=reverse)


def __get_year_distribution_histogram_image_base64(year_interval_to_percentage):
    return __get_attribute_distribution_histogram_image_base64(year_interval_to_percentage,
                                                               "Year of Release", "Year Interval")


def __get_tempo_distribution_histogram_image_base64(tempo_interval_to_percentage):
    #return "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFRUXFxcaGBUVGBgdGBoVGBoXGBcfGBgaHSggGB0lGxoXIjEhJSkrLi4uGh8zODMtNygtLi0BCgoKDg0OGBAPFS0dFh0tLS0tLS0tLS0tKy0tLS0tLS0rLS0tLS0tLS0tLS0tKy0tLSstLS0tLS0tLS0rLS0rLf/AABEIAKQA3AMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAFAAEDBAYCBwj/xAA7EAABAgQEAwUFBgcBAQEAAAABAAIDBBEhBRIxQQZRcSJhgZHwE6GxwdEHFCQyUuEjMzRCYnLxgrIX/8QAGAEBAQEBAQAAAAAAAAAAAAAAAAECAwT/xAAcEQEBAQADAQEBAAAAAAAAAAAAARECMUEhElH/2gAMAwEAAhEDEQA/AN5I/mO2wKklI7GveHOvXTfRVsMiAmo5CuuuqDDM+O9waSA6x6LpfjESxCPammmf5qbH/wCcSeQy9FUjNIJrrVWMRje0bDduKg+FF1vjLxHjA/jI3+30QdE+K31nI5/zd7v+II+YGy897dE6fN6+CpOjnouTEKguOi96v4DAEaYhw60BcPLdAqo7wZEpNwj/AJIr0rEeA4EZn8FzobxYZqFhPhosJCwyJLx3Q4rcr27H5c16/CijKCoMWw1k0zK6giNHYfS9eR7ig84zegvauAD+Dh+P/wBOXjExBdDeWOFHNNCO9ez8Af0cPx+JTgnLppEkkxK6OanN4XCifmYK8xY+ap/co8P+W/OP0xL25V1RlcveBqiggnmtdWNCMN36hdvn5q8Zhr7tII5grqNQ60KDzs0yEaMAq47KKIRXLI/aR/TM/wB/kUZgvLhUoH9on9JD/wBx8FL0s7ebJJJLi6GTpJwUDJJJIPXOF4lW/TxUuCQCXRAd3ml7qpguaGxwFCa/Wqs8NzWcV3JNfXNelyX5iDCL8rj2hTx9BBsUcIZDf7RUg9f3CuY8ykX/AMivvQPGLQs5JtXyFDb1stZZN1HhmMRy+NEdzc4+ZVBWZx9XO6n4qsuDoSSSSDtsInZazhXByHiI+ooagczqi0lg8uZWF7F4dEIqeYO9RsLrRYTw/khE1zOob/SiC/IzVbCvdz6KzDmBWxWXlp/K6h8T0ROLHFK6oq5xJhzZlvt4f8xgHtBzbseq2XAA/Bs8fiV53LYoWPDgeo7ui3vDGJQ2j2IOWtS2u+a9u8LUYvTVArjMTUU+irOBH7JzFNfXyWmViHE2OvzXBdc10F6d48VCDTx9eGqGYxi8OCDU9rZqCHiHGBBZQULzoFlZOI5xLnVJqENizbozy53P3IvKAClbfVYtbkHoMajEI+0Nv4Rn+4+F1NCi1cB3hN9ojKynSIPgU8PXlwSqnXA19ev+Lk27SSTIHSSXOYIPQI+MOgMiZxo3Xap0QSV+0ODALcjC8AUNbeKynEXF4jwiyrjUi9eR96yD4x2K7Xkxj6Li4qJkNi5ctRzrbb5qjxK78M1uxbFv3Bp/ZeXcJY6+DCcc5IB0N7eK1buLWTEpHDm0dChRKGtiX0AtsdVv97xxM+vJohqmbDJ2U8Jtb6K7BlXPAZDFXHU+tFyaQ4fhTorsrRU+7xKITElBhVaTneLUb+UeO6aUa6A8gxKWvlPuJTT0zDbUhtzsgig0Zcmg5A69e5amU4yysEKG22lSSslAAiXcKnYV+CI4fhhDxtS5adQgNueak+v2VqXmnEU17kOisJNAtBgkMMbmeO1tTmsztVJsu8mtDqj0eNZtDRzdDy8V22adEs1lOgViR4diPPaNF0xlcl8fj+yH8QHvp65JoHEUwHVLhQa1CNyeADLlIp8vVVQxfAC06mm6qfFXE+Ln0ysy1OpGoWYnY5IzOcXOJvzV+Ywg5gWja5VKYljSvms1Yhl42VG5WZJsNO/kEDfR1ABTmrbIlAABf1y9WCjTTYE3NEBp2Rp3nf4qf7Q/6P8A9t+BU/DEMOZrUg+5QfaBeTd3Ob81fGb28rBXLaVp3J2lMdR69brk26KSdMAgYlOWjklVRhwvQjX1ugxFUySS6MumPI0Kvy+KFsOJDp/MAB6Ag/JDkkE+d2gV6Wm4jWOaDTNy+qGON1MyMgtykF7na1K7mMOcHdppzHnz7lHLRiDmGo0Rd8y+LDzup2XAVHfuiBsrJlr6OqDsNLrS4SHuNdRoa60C5myyLDgnRxP5gKXFfmAi+Cy3aIdYk6oruDhbi6oqtbheFZ200RjCpWA1ly0ndVcX4ngyooGipNgNFqTGdFZHBGsuaW6IzDhQhvdeP4j9o0QnQAddlNh/FsR9CHHpVXTHs7XDYofiAzhwrrZZfh7HXRSGkopNzTmk8kTFfGZMthtLRoQDTkUExqWDAALk6qfE+IMrSHaLJR+Ky9/ZYXJqyLcSQ0I1p5qaBKjKK/m9aotwzOQo7Ts4atNLK8MPaHGlNdCpi6h4ZeRWhuLJcb3kX1/U34qWXly15pY92hCi4zvIv7nN+KeJ68rgjfqunOHj3Llho3pX4rgu7QXF0WFy76fFcGMFwYyDuKbbXVdO4n1ouVBkEkkl1ZJOmUntT3eSCNdNK7hubuFaiS7KAg39eaBQtFoZKGPucQ7lx8hRBZeWzC0RteR81fdMubB9lS1dQeaAhwxHbEhmC8Dm3qtPCdlFV59JZoTmnyI0P1W6hRczAa10QabD5xmS+qxvFziXNOyIteQFHMQw/sm6umMDMVLjVEsDJDwNijEbA670VzDMC7YIHj7lAXwCOYbwb/8AVufZuiQ6gIXgfDLjc0W3kpMMaAQtxm14/wAYsczK3mT7qLAiI8PIuL7L3vivhL7yWuaaZa23uvP57g6JDe6oBH6u5ZsqyqPC5Lo7Gitx2qLXTcnQ1bEdXqg8s2HLA5BWKbZuXRWsNmXOIzG6T+FHcPjufR2a7RRwXPFzqyL+rfiuIUtEzVZvr0U3FMI/cYlbEU86rV6T15XUUPj81Wzn91JelO+lPooqLg6OjTbyXCfRJQO7lyXKdxumQZBSewd+k+SeBCLjba6tQZ+IwZamneurKvDlSdbK1CwzMQMwSabDor+EwqvHcUBr/wDO4ghe0EQONAcoF0KiYJEbsbcwvZZEfw2f6j4LmPJMdq0JpjxU4bEH9vmoIsB3LyXtTsIhfpCynEWFNabNQx58YzgACTSth60W1wOOHQhVY/EQM/ZWk4ZdVpb3+5CDlKHw+acgVqnonbDsVFWJNmY3R2CGsApQd6zoflv8Fy+bJGvmtys49L4cn2uqOW60LXg6FeCwuJHwXUFQVo+HeMojn5aFx5JOSXi9ZQ3GJdhbVw8V3IzLi1pedRdd4jAzssRZaZebYzKDNYbqjKuDXXstZHkSTp6CqnCG1rRRoTwMh11zxqykpFHcPiFJhkP2YsFT4mi5pWN0SnryAu1G9SVFVSufvTn8veoVwdCTpk6gZMT6omcDzXHtO/zCuIB4dMNYHV1Oik9s1wIPwQ5outJgku0wYpIrYa7dF0QMARjBNfFB0UwOJR9CbW15JR7NJCrG9FbbCqhkni8uGj+I2tOaJMxGCf72+asiU0SHRAOIoNW1PetGZlh/K4HoUMng0ip0Fa7oryGes80buUQwSKQ6gGuqldC9pFdlFW5jQ+KO8O4a1jXxXjSoA2rqkgkISCdxumUHLmHmoXsPNW86pz8+2GNLoKeJSoc01FDqDuivCbWwu0bk7rMzE+9+th3ctlawzEyyzrhTfqvUIOJPpUOHRG8PxRxsaUKwGGYm1wHgtFJxagLcrFgxOjtVafBVodzcefVRu7RF0QkJVx1uBeqqI5hoaAKoNjw/Cxhr2foURn39o9yFYw4/d4w/wKVY8tmG6qsp3vBqdNqdVAuFdCSSSUCVcWsQPFWCuQe5WVGVbqtXgo/Cv2LrevBZFStmHAUBIHJdEWozqEKRp3Q4vKvhVFuDFJOpsrzIpt2jrz6fuqUo1W2G46qKMicewloc4dCoJufeRdz+tbdyLQZVrolT3HyUseQfGPs4bLFJBlsPjOzNFaVcNO9bhxysDASRrfW/NF+H/s8EFjosemYAkU2/ZBo57RVzEQB96LoqGJY1TsincXUaSkoNjjKhFXvVKehEtUGZa9SQnU6qcSx5LqBJHNp6CajR8NsJoaclsoBA5+igOBy2VvL1sjcEaBaiUUlr0Wkw1vZ8FnJVtwFqpFlGhaZrJ4mblDZ0ZoEbvYfqrPG846XfZlQ4anRYae4njFjmta0A1BsfqpbiyM2QQo3OonD7EHVQRInh8VyxtOkomuGylUsCSASTFvqqisllKfIrTIRO23zUzZM/pK6sqXsjyVqGTuFaZIu5eZUrJHm4dEHMCMBqrMJ4NKKVko3n5BaDh7h3272gNJFq05IDeC4PEjlpYLEC4+a9TwfB4cFoo0Ztyda9dlFgOHQpdoY0AUAv396uzs4GA3r6H7rcjFuh/FWJthwnN/ucKU6ry55ui/EGIGLEJJ0QcqcmuMcmirvFDRWHNSe2qw0qtb4rqt7rp8Kl1wqEJUH6K3KyjRQnaiggG6nBQGJb3IjB1Hghck6w5onLm46rUZo3h7KlaeAOyFnsKF1pAVpisf8AaVCDoDBvmPWi8xfJCl/X1XqvHYGRtqlefxISzY3xZOYlaGwVZ0EckXjCpKruhDkuVaDvYBSK77Hei7+6k6Nr0T6B1Ewb18ytBKYFGf8AlhkV3IoiI4Njcm+YSSmvORMO5rn27uZUa6YF0ZdseTrdTQiUwb6srEFmnrooq3h0J0RwaNyLL27hvDxLwmga0FfcsPwVhYYPaPAqfylegysQFooVrjGbV4xa930Wdx2bcKitvqrs5MkCgWVxaMa6rSQLjxakqIuUJfU/unc5c62mqkSodq89v28E7Wm26iunX7lyYa7ypNagdkOi7a2qdgVuBCqfFaxFuQhrQYdJ1oUMk4NwtLIKxmiMCStUbK/BB3XMq6ymWmWN47rVl7UWOIr0W54tlHRHtDb7dDdC5bhqpq40HJStSvPnQKk3VmBg8V5GVjiD3fPRekQOHJcUOSp3JuikOXAFALKflf0wmG8EOcKxXZf8RqtFhnDsKB+XtO5uCPFgXIb8FcTUTYQ5eCf2Q5Luia6qPl9uqmgj15BJJc2lgC/ruRPCGBz2gi1U6SRXpso2gAFgAESkohSSXSdM3txORDVZbFHk1qkkpSBYTsHZqnSWG3UM1KlTpKBJJJILEFuivyY9eaSS0g1KsFfFGJE6JklYzR2T0PgrKSS0yHxW9o+uaic2gSSUU7DYriuqdJAg7RPF9e5JJA7W2r61XbR6skkg/9k="
    # TODO replace dummy image by actual histogram.
    #  -> first, extract re-usable code of __get_year_distribution_histogram_image_base64 first
    return __get_attribute_distribution_histogram_image_base64(tempo_interval_to_percentage,
                                                               "Tempo (BPM)", "Tempo (BPM)")

def __get_attribute_distribution_histogram_image_base64(x_label_to_percentage, attribute_name, x_label_name):
    plt.title(f"{attribute_name} Distribution")
    plt.xlabel(x_label_name) # TODO use attribute_name, no need for different name
    plt.ylabel("Percentage")

    x_labels = []
    y_labels = []
    for x_label, percentage in x_label_to_percentage.items():
        x_labels.append(x_label)
        y_labels.append(percentage)

    plt.bar(x_labels, y_labels, edgecolor="black")
    plt.xticks(rotation=15)
    plt.tight_layout()

    image_buffer = BytesIO()
    plt.savefig(image_buffer, format="png")
    plt.clf()  # Clear the current figure. Else the different figures would be drawn on top of each other.
    image_bytes = image_buffer.getvalue()
    image_base64_bytes = base64.encodebytes(image_bytes)
    image_base64_string = image_base64_bytes.decode("utf8")

    return image_base64_string
