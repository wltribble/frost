from django.contrib import admin

from .models import Job, Field
# Register your models here.

class FieldInLine(admin.TabularInline):
    model = Field
    extra = 0

    readonly_fields = ['field_has_been_set', 'editing_mode']


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created', 'has_process_outline_been_modified_for_this_operation', 'date_submitted', 'has_job_name_been_set', 'completed', 'process_outline']

    fieldsets = [
        (None,          {'fields': ['job_id',]}),
        ('Date Information', {'fields': ['date_created', 'last_update',]}),
        ('Process Information', {'fields': ['process_outline', 'has_process_outline_been_modified_for_this_operation',]}),
        ('Submission Information', {'fields': ['has_job_name_been_set', 'completed', 'date_submitted',]})
    ]
    search_fields = ['job_id', 'job_number', 'assembly_number', 'operation_number',]
    inlines = [FieldInLine]
    list_display = ('job_id', 'date_created', 'completed', 'process_outline', 'has_process_outline_been_modified_for_this_operation')
    list_filter = ['completed', 'date_created', 'process_outline']


admin.site.register(Job, JobAdmin)
