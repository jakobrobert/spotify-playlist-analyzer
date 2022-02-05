source ENV/bin/activate
cd app/ || exit
export FLASK_APP=spotify_playlist_analyzer:app
export FLASK_ENV=development
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=1024
flask run
