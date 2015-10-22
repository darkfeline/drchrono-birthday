from django.conf.urls import patterns, url

from birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
)
