# Copyright (C) 2015-2016  Allen Li
#
# This file is part of drchrono Birthday.
#
# drchrono Birthday is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# drchrono Birthday is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with drchrono Birthday.  If not, see <http://www.gnu.org/licenses/>.

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
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return '{}'.format(self.user)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor)
    name = models.CharField(max_length=256)
    date_of_birth = models.DateField(null=True)
    email = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return '{}'.format(self.name)
