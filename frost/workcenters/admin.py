from django.contrib import admin

from .models import WorkCenter

list_display = ('workcenter_id')

admin.site.register(WorkCenter)
