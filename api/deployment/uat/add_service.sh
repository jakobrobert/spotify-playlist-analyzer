cp ./service.ini ~/etc/services.d/spotify_playlist_analyzer_api_uat.ini
supervisorctl reread
supervisorctl update
