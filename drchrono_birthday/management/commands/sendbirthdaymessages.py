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

from collections import defaultdict
import ConfigParser
import datetime
from email.mime.text import MIMEText
import smtplib
from itertools import chain

from django.core.management.base import BaseCommand

from drchrono_birthday import models


class _ConfigProxy:

    """Proxy class for performing item setting and getting for Config.

    Emulates configparser interface in Python 3.

    """

    def __init__(self, config, section):
        self.config = config
        self.section = section

    def __getitem__(self, key):
        return self.config.get(self.section, key)

    def __setitem__(self, key, value):
        if not self.config.has_section(self.section):
            self.config.add_section(self.section)
        return self.config.set(self.section, key, value)

    def __contains__(self, item):
        return self.config.has_option(self.section, item)


class Config:

    DEF_VALUES = {
        'sendmail': {
            'port': '587',
            'encryption': 'starttls',
            'user': '',
        }
    }
    REQ_VALUES = {
        'sendmail': ['host', 'from'],
    }

    def __init__(self, path):
        self.config = ConfigParser.ConfigParser()
        self._set_defaults()
        self.config.read(path)
        self._check()
        self._valuecheck()

    def __getitem__(self, key):
        return _ConfigProxy(self.config, key)

    def _set_defaults(self):
        for section, pairs in self.DEF_VALUES.items():
            for key, value in pairs.items():
                self[section][key] = value

    def _check(self):
        """Check that all required configuration keys have been provided.

        Raises MissingConfigKeysError.

        """
        missing = defaultdict(list)
        for section in self.REQ_VALUES:
            for key in self.REQ_VALUES[section]:
                if key not in self[section]:
                    missing[section].append(key)
        if missing:
            raise MissingConfigKeysError(missing)

    def _valuecheck(self):
        """Check that no configuration keys have invalid values."""
        option = self['sendmail']['encryption']
        if option not in ('none', 'ssl', 'starttls'):
            raise ConfigValueError('sendmail', 'encryption', option)


class ConfigError(Exception):
    pass


class MissingConfigKeysError(ConfigError):

    def __init__(self, missing):
        self.missing = missing

    def __str__(self):
        return "Missing configuration values: {}".format(
            '; '.join(
                'in [{}], {}'.format(section, ', '.join(self.missing[section]))
                for section in self.missing))


class ConfigValueError(ConfigError):

    def __init__(self, section, key, value):
        self.section = section
        self.key = key
        self.value = value

    def __str__(self):
        msg = "Invalid configuration value: {}.{} = {}"
        return msg.format(self.section, self.key, self.value)


class Command(BaseCommand):

    help = 'Send all birthday messages since last check.'
    _DATE_FMT = '%Y-%m-%d'

    def add_arguments(self, parser):
        parser.add_argument("config", help="Path to configuration file.")

    def handle(self, *args, **options):
        today = datetime.date.today()

        # Check last run date.  If this is the first run, only do today.
        # We use this as a part of a lookup range search, which is inclusive,
        # so we include the day AFTER the last run date.
        try:
            last_sent = models.Global.get(key="last_sent")
        except models.Global.DoesNotExist:
            last_sent = today
        else:
            last_sent = datetime.datetime.strptime(self._DATE_FMT)
            last_sent = last_sent.date() + datetime.timedelta(days=1)

        # Quit if sent for today already.
        if last_sent > today:
            return

        # We limit to a week old, so we don't send messages that are half a
        # year late.  We subtract by 6 because range is inclusive.
        last_sent = max(last_sent, today - datetime.timedelta(days=6))

        patients = self._get_patients(last_sent, today)

        # Send emails.
        config = Config(options['config'])
        config = config['sendmail']
        smtp = self._configure_smtp(config)

        for patient in patients:
            if patient.email:
                doctor = patient.doctor
                msg = doctor.message
                self._send_mail(smtp, config['from'], patient.email,
                                msg.format(doctor=doctor.name,
                                           patient=patient.name))

        smtp.quit()

        # Update last sent date.
        last_sent = models.Global(key="last_sent",
                                  value=today.strftime(self._DATE_FMT))

    @staticmethod
    def _get_patients(last_sent, today):
        # We select all patients whose birthdays fall within our range.  This
        # is a bit tricky.
        #
        # There are two cases: Range is within one month and range is broken up
        # across two months.
        if last_sent.month == today.month:  # same month
            patients = models.Patient.objects.filter(
                date_of_birth__day__gte=last_sent.day,
                date_of_birth__day__lte=today.day,
            )
        else:  # two different months
            patients = chain(
                models.Patient.objects.filter(
                    date_of_birth__month=last_sent.month,
                    date_of_birth__day__gte=last_sent.day,
                ),
                models.Patient.objects.filter(
                    date_of_birth__month=today.month,
                    date_of_birth__day__lte=today.day,
                ),
            )
        return patients

    @staticmethod
    def _configure_smtp(config):
        """Configure and return SMTP client."""
        config = config['sendmail']

        if config['encryption'] == 'ssl':
            protocol = smtplib.SMTP_SSL
        else:
            protocol = smtplib.SMTP
        smtp = protocol(config['host'], config['port'])

        if config['encryption'] == 'starttls':
            smtp.starttls()

        if config['user']:
            smtp.login(config['user'], config['password'])

        return smtp

    @staticmethod
    def _send_mail(smtp, from_addr, to_addr, message):
        "Send an email using an SMTP session."
        msg = MIMEText(message)
        msg['Subject'] = 'Happy Birthday!'
        msg['From'] = from_addr
        msg['To'] = to_addr
        smtp.sendmail(from_addr, [to_addr], msg.as_string())
