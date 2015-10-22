from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=256)
    birthday = models.DateField()
    email = models.CharField(max_length=256)

    def __unicode__(self):
        return "{}".format(self.name)
