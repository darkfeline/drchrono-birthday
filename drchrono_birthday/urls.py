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

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from drchrono_birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.index), name='index'),
    url(r'^setup/$', login_required(views.setup), name='setup'),
    url(r'^update/$', login_required(views.update), name='update'),
    url(r'^auth_return/$', login_required(views.auth_return),
        name='auth_return'),
)
