from __future__ import unicode_literals

from django.contrib import admin

from drchrono_birthday import models


admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.FlowModel)
