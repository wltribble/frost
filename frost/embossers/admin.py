from django.contrib import admin

from .models import Job, Field
# Register your models here.

class FieldInLine(admin.TabularInline):
    model = Field
    extra = 0


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created']

    fieldsets = [
        (None,          {'fields': ['job_id']}),
        ('Date Information', {'fields': ['date_created', 'date_due', 'last_update']}),
    ]
    search_fields = ['job_id']
    inlines = [FieldInLine]
    list_display = ('job_id', 'date_created', 'was_created_recently')
    list_filter = ['date_created']


admin.site.register(Job, JobAdmin)
