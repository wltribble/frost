from django.contrib import admin

from .models import Job, Field


class FieldInLine(admin.TabularInline):
    readonly_fields = ['is_associated_with_a_template']

    model = Field
    extra = 0

class GrinderJobAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['job_number', 'assembly_number', 'operation_number']}),
    ]
    inlines = [FieldInLine]
    search_fields = ['job_number']
    list_display = ('operation_number', 'assembly_number', 'job_number', 'job_type', 'completed')
    list_filter = ['completed', 'job_type', 'date_created', 'date_due',]


admin.site.register(Job, GrinderJobAdmin)
