from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Job, Field
# Create your views here.


class IndexView(generic.ListView):
    template_name = 'embossers/index.html'
    context_object_name = 'latest_job_list'

    def get_queryset(self):
        """Return the last 5 created jobs (not including those
        set to be created in the future)."""
        return Job.objects.filter(
            date_created__lte=timezone.now()
        ).order_by('-date_created')[:5]


class DetailView(generic.DetailView):
    model = Job
    template_name = 'embossers/detail.html'

    def get_queryset(self):
        return Job.objects.filter(date_created__lte=timezone.now())



def save_data(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    for jobs in job._meta.get_fields():
        try:
            job_field_count += 1
        except:
            job_field_count = 1
        field_name = 'save_field' + str(job_field_count)
        if field_name in request.POST:
            print ('save field ' + str(job_field_count))
            return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
        elif ('save_field' + str(job_field_count + 1)) in request.POST:
            print ('save field ' + str(job_field_count + 1))
            return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    else:
        return HttpResponseRedirect(reverse('embossers:index'))

def edit_data(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    for jobs in job._meta.get_fields():
        try:
            job_field_count += 1
        except:
            job_field_count = 1
        field_name = 'edit_field' + str(job_field_count)
        if field_name in request.POST:
            print ('edit field ' + str(job_field_count))
            return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
        elif ('edit_field' + str(job_field_count + 1)) in request.POST:
            print ('edit field ' + str(job_field_count + 1))
            return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    else:
        return HttpResponseRedirect(reverse('embossers:index'))

def add_field(request, job_id):
    print ('Add field')
    job = get_object_or_404(Job, pk=job_id)
    for jobs in job._meta.get_fields():
        try:
            job_field_count += 1
        except:
            job_field_count = 1
    new_field_job = job
    new_field_id = str(job_field_count + 1)
    new_field_text = ""
    field = Field.objects.create_field(new_field_job, new_field_id, new_field_text)
    return HttpResponseRedirect(reverse('embossers:index'))
