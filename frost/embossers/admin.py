from django.contrib import admin

from .models import Job, Field
# Register your models here.

class FieldInLine(admin.TabularInline):
    model = Field
    extra = 0

    readonly_fields = ['field_has_been_set', 'editing_mode']


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created', 'has_process_outline_been_modified_for_this_operation',]

    fieldsets = [
        (None,          {'fields': ['job_id',]}),
        ('Date Information', {'fields': ['date_created', 'last_update', 'date_submitted',]}),
        ('Process Information', {'fields': ['process_outline', 'has_process_outline_been_modified_for_this_operation',]}),
    ]
    search_fields = ['job_id']
    inlines = [FieldInLine]
    list_display = ('job_id', 'date_created', 'was_created_recently')
    list_filter = ['date_created']


admin.site.register(Job, JobAdmin)
