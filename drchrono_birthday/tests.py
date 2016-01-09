# Copyright (C) 2016  Allen Li
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

import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from drchrono_birthday import models
from drchrono_birthday.management.commands.sendbirthdaymessages \
    import Command


class GetPatientsTest(TestCase):

    def setUp(self):
        bob = User.objects.create_user('bob', 'bob@example.com', 'bob')
        bob.save()
        doctor = models.Doctor(user=bob, name='Bob',
                               last_updated=timezone.now())
        doctor.save()
        self.doctor = doctor

    def make_patient(self, name, dob):
        patient = models.Patient(doctor=self.doctor, name=name,
                                 date_of_birth=dob)
        patient.save()

    def test_day(self):
        """Test when range is one day long."""
        self.make_patient('A', datetime.date(1990, 12, 31))
        self.make_patient('B', datetime.date(1990, 1, 1))
        self.make_patient('C', datetime.date(1990, 1, 2))
        patients = Command._get_patients(datetime.date(2000, 1, 1),
                                         datetime.date(2000, 1, 1))
        patients = [x.name for x in patients]
        self.assertNotIn('A', patients)
        self.assertIn('B', patients)
        self.assertNotIn('C', patients)

    def test_week_in_month(self):
        """Test when range is one week long within a month."""
        self.make_patient('A', datetime.date(1990, 6, 5))
        self.make_patient('B', datetime.date(1990, 6, 6))
        self.make_patient('C', datetime.date(1990, 6, 12))
        self.make_patient('D', datetime.date(1990, 6, 13))
        start = datetime.date(2000, 6, 6)
        end = start + datetime.timedelta(days=6)  # inclusive
        patients = Command._get_patients(start, end)
        patients = [x.name for x in patients]
        self.assertNotIn('A', patients)
        self.assertIn('B', patients)
        self.assertIn('C', patients)
        self.assertNotIn('D', patients)

    def test_week_split(self):
        """Test when range is one week long split across months."""
        self.make_patient('A', datetime.date(1990, 6, 27))
        self.make_patient('B', datetime.date(1990, 6, 28))
        self.make_patient('C', datetime.date(1990, 6, 30))
        self.make_patient('D', datetime.date(1990, 7, 1))
        self.make_patient('E', datetime.date(1990, 7, 4))
        self.make_patient('F', datetime.date(1990, 7, 5))
        start = datetime.date(2000, 6, 28)
        end = start + datetime.timedelta(days=6)  # inclusive
        patients = Command._get_patients(start, end)
        patients = [x.name for x in patients]
        self.assertNotIn('A', patients)
        self.assertIn('B', patients)
        self.assertIn('C', patients)
        self.assertIn('D', patients)
        self.assertIn('E', patients)
        self.assertNotIn('F', patients)
