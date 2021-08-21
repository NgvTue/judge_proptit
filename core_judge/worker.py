from logging import log
import logging
import os
import time

from celery import Celery
import json
from job.OutputOnly import OutputOnly
from config import env

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        pass
    def on_failure(self, exc, task_id, args, kwargs):
        pass

@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@celery.task(name='judge',bind=True, base=CallbackTask)
def judge_session(self,job_description):
    wo = OutputOnly(job_description, celery_task_object=self)
    result =  wo.run()
    return result

    