from django.contrib import admin

from birthday.models import Patient


class PatientAdmin(admin.ModelAdmin):
    fields = ['name', 'birthday', 'email']
    list_display = ['name', 'birthday', 'email']
    search_fields = ['name']

# Register your models here.
admin.site.register(Patient, PatientAdmin)
