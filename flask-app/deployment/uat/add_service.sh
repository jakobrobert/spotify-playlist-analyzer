cp ./service.ini ~/etc/services.d/spotify_playlist_analyzer_uat.ini
supervisorctl reread
supervisorctl update
