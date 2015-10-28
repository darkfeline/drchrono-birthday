from __future__ import unicode_literals

from django.contrib import admin

from drchrono_birthday import models


class PatientAdmin(admin.ModelAdmin):
    fields = ['name', 'birthday', 'email']
    list_display = ['name', 'birthday', 'email']
    search_fields = ['name']

# Register your models here.
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Doctor)
admin.site.register(models.FlowModel)
