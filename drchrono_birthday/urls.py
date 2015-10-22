from django.conf.urls import patterns, url

from drchrono_birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
)
