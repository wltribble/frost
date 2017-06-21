from django.contrib import admin

from .models import Job, Field
# Register your models here.

class FieldInLine(admin.TabularInline):
    model = Field
    extra = 0

    readonly_fields = ['field_has_been_set', 'editing_mode']


class JobAdmin(admin.ModelAdmin):
    # readonly_fields = ['date_created', 'has_process_outline_been_modified_for_this_operation', 'date_submitted', 'has_job_name_been_set', 'completed', 'process_outline']

    fieldsets = [
        (None,          {'fields': ['jmojobid','jmojobassemblyid', 'jmojoboperationid']}),
        ('Date Information', {'fields': ['jmocreateddate',]}),
        # ('Process Information', {'fields': ['process_outline', 'has_process_outline_been_modified_for_this_operation',]}),
        # ('Submission Information', {'fields': ['has_job_name_been_set', 'completed', 'date_submitted',]})
    ]
    search_fields = ['jmojobid', 'jmojobassemblyid', 'jmojoboperationid',]
    inlines = [FieldInLine]
    list_display = ('jmojobid', 'jmojobassemblyid', 'jmojoboperationid', 'jmocreateddate',)
    list_filter = []


admin.site.register(Job, JobAdmin)
