from django.db import models

# Create your models here.


class Sites(models.Model):
    url = models.URLField(unique=True)


class MalwareSites(models.Model):
    url = models.URLField(unique=True)


class PhishingSites(models.Model):
    url = models.URLField(unique=True)
