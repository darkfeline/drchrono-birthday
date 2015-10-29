import datetime
import smtplib
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand

from drchrono_birthday import models


class Command(BaseCommand):
    help = 'Send birthday messages for today.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        smtp = configure_smtp()
        today = datetime.date.today()
        patients = models.Patient.objects.filter(
            date_of_birth__month=today.month,
            date_of_birth__day=today.day,
        )
        for doctor in models.Doctor.objects.all():
            message = doctor.message
            doctor_name = doctor.name
            for patient in patients.filter(doctor=doctor):
                if patient.email:
                    _send_mail(smtp, _FROM_ADDR, patient.email,
                               message.format(doctor=doctor_name,
                                              patient=patient.name))
        smtp.quit()


_FROM_ADDR = 'bob@example.com'


def configure_smtp():
    """Configure SMTP sending here."""
    pass


def _send_mail(smtp, from_addr, to_addr, message):
    msg = MIMEText(message)
    msg['Subject'] = 'Happy Birthday!'
    msg['From'] = from_addr
    msg['To'] = to_addr
    smtp.sendmail(from_addr, [to_addr], msg.as_string())
