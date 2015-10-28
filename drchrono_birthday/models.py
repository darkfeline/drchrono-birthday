from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import FlowField

_DEFAULT_MESSAGE = """Dear {patient},

Happy birthday!

Sincerely,
{doctor}"""


class FlowModel(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    flow = FlowField()

    def __unicode__(self):
        return '{}'.format(self.user)


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=256)
    message = models.TextField(default=_DEFAULT_MESSAGE)

    def __unicode__(self):
        return '{}'.format(self.user)


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    name = models.CharField(max_length=256)
    birthday = models.DateField()
    email = models.CharField(max_length=256)

    def __unicode__(self):
        return '{}'.format(self.name)
