from celery import Celery
from celery import shared_task
from django.core.management import call_command


@shared_task
def delete_tokens():

    call_command('flushexpiredtokens', verbosity=0)

