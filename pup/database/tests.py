from django.test import TestCase
from celery import shared_task
from django.core.management import call_command

# Create your tests here.


@shared_task
def parse_sites_task():
    call_command('parse_sites')