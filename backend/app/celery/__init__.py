import os
from celery import Celery


def create_celery(app_name=__name__):
    # Use new-style config keys pulled from environment variables
    return Celery(
        app_name,
        broker=os.environ.get("broker_url", "redis://redis:6379/0"),
        backend=os.environ.get("CELERY_BACKEND"),
        broker_connection_retry_on_startup=os.environ.get("broker_connection_retry_on_startup", "True") == "True"
    )


def init_celery(celery, app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
