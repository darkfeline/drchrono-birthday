from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from drchrono_birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.index), name='index'),
    url(r'^update/$', login_required(views.update), name='update'),
    url(r'^auth_return/$', login_required(views.auth_return),
        name='auth_return'),
)
