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
def operations_by_job(job, report):
    jobs = Job.objects.all().filter(jmojobid=job)
    return {'operations': jobs, 'report': report, 'job': job}

@register.inclusion_tag('jobs/misc/fields_by_operation.html')
def fields_by_operation(job, assembly, operation, report, loop_counter):
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
    return {'fields_needed': fields_needed, 'report': report, 'loop_counter': loop_counter, 'job': job, 'assembly': assembly, 'operation': operation.jmojoboperationid}

@register.inclusion_tag('jobs/misc/fields_for_report.html')
def fields_for_report(job, fields):
    operations = Job.objects.all().filter(jmojobid=job)
    job = job
    fields = fields
    return {'operations': operations, 'job': job, 'fields': fields}

@register.inclusion_tag('jobs/misc/fields_by_operation_for_report.html')
def fields_by_operation_for_report(job, assembly, operation):
    job = Job.objects.all().filter(jmojobid=job).filter(jmojobassemblyid=assembly).filter(jmojoboperationid=operation).get()
    job_uuid = job.jmouniqueid

    fields_needed = []
    field_ids = []
    for item in fields:
        if fields[item][0] = job and fields[item][1] = assembly and fields[item][2] = operation:
            field_ids.append(fields[item][3])
    print (field_ids)
    for field in Field.objects.all().filter(job=job_uuid):
        for field_id in field_ids:
            if field.id == field_id:
                fields_needed.append(field)
            else:
                pass
    return {'fields_needed': fields_needed}
