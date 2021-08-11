from celery import Celery
from app import app

CELERY_TASK_LIST = [
    'main.tasks'
]


def make_celery():
    celery = Celery(broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    include=CELERY_TASK_LIST)

    celery.conf.task_routes = {
        'web.*': {'queue': 'web'}
    }

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
