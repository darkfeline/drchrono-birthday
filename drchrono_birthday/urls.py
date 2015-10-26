from django.conf.urls import patterns, url

from drchrono_birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^update/$', views.update, name='update'),
    url(r'^auth_return/$', views.auth_return, name='auth_return'),
)
