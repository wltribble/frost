from django.contrib import admin

from .models import Job, Field, Process, OutlineField
# Register your models here.

class FieldInLine(admin.TabularInline):
    model = Field
    extra = 0

    readonly_fields = ['field_has_been_set', 'editing_mode']


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created', 'has_process_outline_been_modified',]

    fieldsets = [
        (None,          {'fields': ['job_id',]}),
        ('Date Information', {'fields': ['date_created', 'last_update',]}),
        ('Procedure Information', {'fields': ['process_outline', 'has_process_outline_been_modified',]}),
    ]
    search_fields = ['job_id']
    inlines = [FieldInLine]
    list_display = ('job_id', 'date_created', 'was_created_recently')
    list_filter = ['date_created']


class OutlineFieldInLine(admin.TabularInline):
    model = OutlineField
    extra = 0

class ProcessAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['job_id',]}),
    ]
    inlines = [OutlineFieldInLine]
    list_display = ('process_name')





admin.site.register(Job, JobAdmin)
