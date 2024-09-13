from celery import Celery
from api import create_app
from api.models import db
from api.config import Config

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=Config.result_backend,
        broker=Config.broker_url
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Create an app instance without routes to avoid circular imports
flask_app = create_app()
celery = make_celery(flask_app)
