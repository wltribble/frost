from django import template

from jobs.models import Job, Field

register = template.Library()

@register.inclusion_tag('jobs/misc/fields_by_center.html')
def fields_by_center(job, center):
    jobs = Job.objects.all().filter(jmojobid=job)

    counter = 0
    fields_needed = []
    for operation in jobs:
        for field in Field.objects.all().filter(job=operation.jmouniqueid):
            if int(field.submission_number) > counter:
                counter = int(field.submission_number)
            else:
                pass
        fields_needed.append(Field.objects.all().filter(job=operation.jmouniqueid).filter(is_a_meta_field=False).filter(submission_number=counter))
    return fields_needed
