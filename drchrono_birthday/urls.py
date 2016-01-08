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

from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from drchrono_birthday import views

urlpatterns = patterns(
    '',
    url(r'^$', login_required(views.index), name='index'),
    url(r'^setup/$', login_required(views.setup), name='setup'),
    url(r'^update/$', login_required(views.update), name='update'),
    url(r'^message/$', login_required(views.message), name='message'),
    url(r'^auth_return/$', login_required(views.auth_return),
        name='auth_return'),
)
