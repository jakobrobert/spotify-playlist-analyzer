source ENV/bin/activate
cd app/ || exit
export FLASK_APP=spotify_playlist_analyzer_api:app
export FLASK_ENV=production
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=1025
flask run
