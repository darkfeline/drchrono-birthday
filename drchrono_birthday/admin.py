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

from django.contrib import admin

from drchrono_birthday import models


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'name', 'date_of_birth', 'email')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')


class FlowModelAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.FlowModel, FlowModelAdmin)
