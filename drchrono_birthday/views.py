# Copyright (C) 2015  Allen Li
#
# This file is part of drchrono_birthday.
#
# drchrono_birthday is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# drchrono_birthday is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with drchrono_birthday.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import json
import datetime

from django.shortcuts import render
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.http import HttpResponseForbidden
from django.core import urlresolvers
from django.template import loader as template_loader

import httplib2
from oauth2client import client

from drchrono_birthday.models import FlowModel
from drchrono_birthday.models import Doctor
from drchrono_birthday.models import Patient
from drchrono_birthday.forms import MessageForm

SECRETS_PATH = 'client_secrets.json'


class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303


def _make_flow():
    """Make flow object for OAuth."""
    return client.flow_from_clientsecrets(
        SECRETS_PATH,
        scope='patients user',
        redirect_uri='http://localhost:8000/birthday/auth_return/',
    )


def _render_error(status, message):
    """Render template for error page."""
    template = template_loader.get_template('drchrono_birthday/error.html')
    context = {
        'status': status,
        'message': message,
    }
    return template.render(context)


def index(request):
    """Handle main page."""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    try:
        current_doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        index_uri = urlresolvers.reverse('drchrono_birthday:setup')
        return HttpResponseSeeOther(index_uri)
    last_updated_text = 'Patient data last updated on {0:%x} at {0:%X}.'
    last_updated_text = last_updated_text.format(current_doctor.last_updated)
    context = {'name': current_doctor.name,
               'user': current_doctor.user,
               'last_updated': last_updated_text,
               'message_form': MessageForm(
                   initial={'message': current_doctor.message})}
    return render(request, 'drchrono_birthday/index.html', context)


def setup(request):
    """Handle initial user setup."""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    context = {'user': request.user}
    return render(request, 'drchrono_birthday/setup.html', context)


def update(request):
    """Handle requests to update database using drchrono API."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    flow = _make_flow()
    auth_uri = flow.step1_get_authorize_url()
    FlowModel(user=request.user, flow=flow).save()
    return HttpResponseSeeOther(auth_uri)


def message(request):
    """Handle requests to update user message."""
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        current_doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return HttpResponseForbidden()
    current_doctor.message = request.POST['message']
    current_doctor.save()
    index_uri = urlresolvers.reverse('drchrono_birthday:index')
    return HttpResponseSeeOther(index_uri)


def auth_return(request):
    """Handle OAuth return."""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Get credentials.
    flow = FlowModel.objects.get(user=request.user).flow
    if 'error' in request.GET:
        return HttpResponseServerError(
            _render_error(500, request.GET['error']))
    auth_code = request.GET['code']
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())

    # Update info.
    # Get doctor id.
    resp, content = http_auth.request('https://drchrono.com/api/users/current')
    if resp.status != 200:
        return HttpResponseServerError(
            _render_error(500, resp.reason))
    data = json.loads(content)
    doctor_id = data['doctor']

    # Get doctor name.
    resp, content = http_auth.request(
        'https://drchrono.com/api/doctors/{}'.format(doctor_id))
    if resp.status != 200:
        return HttpResponseServerError(
            _render_error(500, resp.reason))
    data = json.loads(content)
    name = ' '.join((data['first_name'], data['last_name']))
    doctor = Doctor(user=request.user, name=name, last_updated=datetime.datetime.now())
    doctor.save()

    # Update patients.
    next = 'https://drchrono.com/api/patients'
    while next:
        resp, content = http_auth.request(next)
        if resp.status != 200:
            return HttpResponseServerError(
                _render_error(500, resp.reason))
        data = json.loads(content)

        for patient in data['results']:
            Patient(id=patient['id'],
                    doctor=doctor,
                    name=' '.join((patient['first_name'],
                                   patient['last_name'])),
                    date_of_birth=patient['date_of_birth'],
                    email=patient['email']).save()
        next = data['next']

    # Revoke credentials.
    # drchrono does not have revoke_uri
    # credentials.revoke(httplib2.Http())

    # 303 redirect to main page.
    index_uri = urlresolvers.reverse('drchrono_birthday:index')
    return HttpResponseSeeOther(index_uri)
