from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic

from jobs.models import Job, JobInstructions, AssemblyInstructions

from .models import WorkCenter, Worker, Operation
# Create your views here.

class PickCenterView(generic.ListView):
    template_name = 'jobs/pages/pick_center.html'
    model = WorkCenter

    def get_queryset(self):
        return WorkCenter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickCenterView, self).get_context_data(**kwargs)
        context['workcenters'] = WorkCenter.objects.all().exclude(
                                                            workcenter_id='ENG'
                                                            ).order_by(
                                                                'workcenter_id'
                                                            )
        return context


class EngineeringIndexView(generic.ListView):
    template_name = 'jobs/pages/engineering_index.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search_box', '')
        return Job.objects.all().filter(jmojobid__icontains=search_query)

    def get_context_data(self, **kwargs):
        context = super(EngineeringIndexView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search_box', '')
        jobs = (Job.objects.all().filter(
                                    jmojobid__icontains=search_query
                                    ).order_by('-jmocreateddate')
                                    )
        unique_job_ids = []
        for job in jobs:
            if job.jmojobid != '':
                unique_job_ids.append((job.jmojobid).strip())
        unique_job_ids = set(unique_job_ids)
        unique_job_ids = list(unique_job_ids)
        unique_job_ids_final = [s for s in unique_job_ids if len(s) != 0]
        context['jobs'] = unique_job_ids_final
        return context


class EngineeringPickOperationView(generic.ListView):
    template_name = 'jobs/pages/engineering_pick_operation.html'

    def get_queryset(self, **kwargs):
        job = self.kwargs['jobid']
        return Job.objects.all().filter(jmojobid__icontains=job)

    def get_context_data(self, **kwargs):
        context = super(EngineeringIndexView, self).get_context_data(**kwargs)
        job = self.kwargs['jobid']
        jobs = Job.objects.all().filter(jmojobid__icontains=job)
        context['jobs'] = jobs
        return context


class EngineeringDetailView(generic.DetailView):
    template_name = 'jobs/pages/engineering_detail.html'

    def get_object(self, **kwargs):
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        return job

    def get_context_data(self, **kwargs):
        context = super(EngineeringDetailView, self).get_context_data(**kwargs)
        job = Job.objects.get(jmouniqueid = self.kwargs['urluniqueid'])
        context['job'] = job
        context['fields'] = (Field.objects.all().filter(
                                job=self.kwargs['urluniqueid']).filter(
                                is_a_meta_field=False)
                                )
        context['urluniqueid'] = self.kwargs['urluniqueid']
        context['metafields'] = (Field.objects.all().filter(
                                    job=self.kwargs['urluniqueid']
                                    ).filter(is_a_meta_field=True)
                                    )
        context['reopen_number'] = (
                                    range(1, 2 + int(
                                    Field.objects.all().filter(
                                    job=self.kwargs['urluniqueid']
                                    ).filter(
                                    field_name="reopens"
                                    ).get().field_text))
                                    )
        context['center'] = job.jmoworkcenterid
        context['job_instructions'] = (
                                    JobInstructions.objects.all(
                                    ).filter(
                                    jobid=job.jmojobid)
                                    )
        context['assembly_instructions'] = (
                                AssemblyInstructions.objects.all(
                                ).filter(
                                jobid=job.jmojobid).filter(
                                assemblyid=job.jmojobassemblyid)
                                )
        return context
