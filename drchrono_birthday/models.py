from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    message = models.TextField()


class Patient(models.Model):
    doctor = models.ForeignKey(Doctor)
    name = models.CharField(max_length=256)
    birthday = models.DateField()
    email = models.CharField(max_length=256)

    def __unicode__(self):
        return "{}".format(self.name)
