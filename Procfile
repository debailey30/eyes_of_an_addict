web: gunicorn "Eyes-of-an-Addict.app:create_app()" --workers 3 --bind 0.0.0.0:$PORT
worker: rq worker default
