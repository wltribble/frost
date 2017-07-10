from django import template

from jobs.models import Job, Field

register = template.Library()

@register.inclusion_tag('jobs/misc/fields_by_center.html')
def fields_by_center(job, center):
    jobs = Job.objects.all().filter(jmojobid=job).filter(jmoworkcenterid=center)

    counter = 0
    fields_needed = []
    for operation in jobs:
        for field in Field.objects.all().filter(job=operation.jmouniqueid):
            if int(field.submission_number) > counter:
                counter = int(field.submission_number)
            else:
                pass
        for field in Field.objects.all().filter(job=operation.jmouniqueid).filter(is_a_meta_field=False).filter(submission_number=counter):
            fields_needed.append(field)
    return {'fields_needed': fields_needed, 'center': center}

@register.inclusion_tag('jobs/misc/operations_by_job.html')
def operations_by_job(job):
    jobs = Job.objects.all().filter(jmojobid=job)
    return {'operations': jobs}

@register.inclusion_tag('jobs/misc/fields_by_operation.html')
def fields_by_operation(job, assembly, operation):
    jobs = Job.objects.all().filter(jmojobid=job).filter(jmojobassemblyid=assembly).filter(jmojoboperationid=operation)

    counter = 0
    fields_needed = []
    for operation in jobs:
        for field in Field.objects.all().filter(job=operation.jmouniqueid):
            if int(field.submission_number) > counter:
                counter = int(field.submission_number)
            else:
                pass
        for field in Field.objects.all().filter(job=operation.jmouniqueid).filter(is_a_meta_field=False).filter(submission_number=counter):
            fields_needed.append(field)
    return {'fields_needed': fields_needed}
