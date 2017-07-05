from django.contrib import admin

from .models import Job, Field
# Register your models here.

class FieldAdmin(admin.ModelAdmin):

    fieldsets = [(None, {'fields': ['job', 'field_name', 'field_text', 'required_for_full_submission', 'text_is_operator_editable', 'name_is_operator_editable', 'field_has_been_set']}),]


class JobAdmin(admin.ModelAdmin):
    # readonly_fields = ['date_created', 'has_process_outline_been_modified_for_this_operation', 'date_submitted', 'has_job_name_been_set', 'completed', 'process_outline']

    fieldsets = [
        (None,          {'fields': ['jmojobid','jmojobassemblyid', 'jmojoboperationid']}),
        ('Date Information', {'fields': ['jmocreateddate',]}),
        # ('Process Information', {'fields': ['process_outline', 'has_process_outline_been_modified_for_this_operation',]}),
        # ('Submission Information', {'fields': ['has_job_name_been_set', 'completed', 'date_submitted',]})
    ]
    search_fields = ['jmojobid', 'jmojobassemblyid', 'jmojoboperationid',]
    list_display = ('jmojobid', 'jmojobassemblyid', 'jmojoboperationid', 'jmocreateddate',)
    list_filter = []


admin.site.register(Job, JobAdmin)
admin.site.register(Field, FieldAdmin)
