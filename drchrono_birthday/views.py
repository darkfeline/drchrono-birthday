from django.shortcuts import render

import httplib2
from oauth2client import client

SECRETS_PATH = 'client_secrets.json'


def index(request):
    context = {'name': request.user}
    return render(request, 'drchrono_birthday/index.html', context)


def update(request):
    flow = client.flow_from_clientsecrets(
        SECRETS_PATH,
        scope='',
        redirect_uri='http://localhost/auth_return/',
    )
    auth_uri = flow.step1_get_authorize_url()
    # redirect to auth_uri 303


def auth_return(request):
    flow = client.flow_from_clientsecrets(
        SECRETS_PATH,
        scope='',
        redirect_uri='http://localhost/auth_return/',
    )
    auth_code = request.code  # GET param
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    # authenticate
    # update
    # revoke
    # redirect to root 303
    pass
