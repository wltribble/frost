from django.utils import timezone

from legacy.models import Joboperations
from jobs.models import Job, Field

for old_instance in Joboperations.objects.all():
    job_number = old_instance.jmojobid
    assembly_number = old_instance.jmojobassemblyid
    operation_number = old_instance.jmojoboperationid
    try:
        date_created = old_instance.jmocreateddate
    except:
        date_created = timezone.now()
    last_update = timezone.now()
    job_id = str(job_number) + " -- " + str(assembly_number) + " -- " + str(operation_number)

    new_model = Job.objects.update_or_create(
        job_id=job_id,
        defaults={
            'date_created': date_created, 'last_update': last_update, 'job_number': job_number, 'assembly_number': assembly_number, 'operation_number': operation_number,
        }
    )
