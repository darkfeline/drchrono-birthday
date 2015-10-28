from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.core import urlresolvers
from django.template import RequestContext
from django.template import loader as template_loader

import httplib2
from oauth2client import client

from drchrono_birthday.models import FlowModel
from drchrono_birthday.models import Doctor

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
    context = {'name': request.user}
    return render(request, 'drchrono_birthday/index.html', context)


def update(request):
    flow = _make_flow()
    auth_uri = flow.step1_get_authorize_url()
    FlowModel(user=request.user, flow=flow).save()
    return HttpResponseSeeOther(auth_uri)


def auth_return(request):

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
    Doctor(user=request.user, name=name).save()

    # Update patients.

    # Revoke credentials.
    # drchrono does not have revoke_uri
    # credentials.revoke(httplib2.Http())

    # 303 redirect to main page.
    index_uri = urlresolvers.reverse('drchrono_birthday:index')
    return HttpResponseSeeOther(index_uri)
