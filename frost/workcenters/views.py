from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic

from jobs.models import Job

from .models import WorkCenter, Worker, Operation
# Create your views here.

class PickCenterView(generic.ListView):
    template_name = 'jobs/pages/pick_center.html'
    model = WorkCenter

    def get_queryset(self):
        return WorkCenter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickCenterView, self).get_context_data(**kwargs)
        context['workcenters'] = WorkCenter.objects.all()
        return context


class EngineeringIndexView(generic.ListView):
    template_name = 'jobs/pages/engineering_index.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search_box', '')
        return Job.objects.all().filter(jmojobid__icontains=search_query)

    def get_context_data(self, **kwargs):
        context = super(EngineeringIndexView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search_box', '')
        jobs = Job.objects.all().filter(jmojobid__icontains=search_query)
        unique_job_ids = []
        for job in jobs:
            if job.jmojobid != '':
                unique_job_ids.append((job.jmojobid).strip())
        unique_job_ids = set(unique_job_ids)
        unique_job_ids = list(unique_job_ids)
        unique_job_ids_final = [s for s in unique_job_ids if len(s) != 0]
        context['jobs'] = unique_job_ids_final
        return context
