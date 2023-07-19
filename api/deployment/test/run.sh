source ENV/bin/activate
export FLASK_APP=spotify_playlist_analyzer_api:app
export FLASK_ENV=development
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=5003
flask run
