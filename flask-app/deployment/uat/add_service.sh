cp ./service.ini ~/etc/services.d/spotify_playlist_analyzer_test.ini
supervisorctl reread
supervisorctl update
