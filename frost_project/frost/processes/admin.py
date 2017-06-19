from django.contrib import admin

from .models import Process, OutlineField
# Register your models here.

class OutlineFieldInLine(admin.TabularInline):
    model = OutlineField
    extra = 0

class ProcessAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['process_name',]}),
    ]
    inlines = [OutlineFieldInLine]
    list_display = ('process_name', 'process_date_created')


admin.site.register(Process, ProcessAdmin)
