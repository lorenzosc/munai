#!/bin/sh

flask db upgrade

if [ "$FLASK_ENV" = "development" ]; then
    echo "Running in development mode"
    exec flask run --host=0.0.0.0 --port=5000
else
    echo "Running in production mode"
# gunicorn not installed for production command exec gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
fi
