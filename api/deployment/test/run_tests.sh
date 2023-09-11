source ENV/bin/activate
cd ./tests/ || exit
pytest --verbose --durations=0
deactivate
