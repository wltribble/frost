from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from processes.models import Process
from embossers.models import Job as EmbosserJob
from embossers.models import Field as EmbosserJobField

from .models import Job, Field


class IndexView(generic.ListView):
    template_name = 'grinder_manager/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['jobs'] = EmbosserJob.objects.all()
        for job in context['jobs']:
            if job.completed == False:
                try:
                    context['incomplete_jobs'].append(job)
                except:
                    context['incomplete_jobs'] = []
                    context['incomplete_jobs'].append(job)
            if job.completed == True:
                try:
                    context['complete_jobs'].append(job)
                except:
                    context['complete_jobs'] = []
                    context['complete_jobs'].append(job)
        return context

    def get_queryset(self):
        return EmbosserJob.objects.all()

class GrinderJobSetup(generic.DetailView):
    model = Job
    template_name = 'grinder_manager/pages/setup.html'

    def get_queryset(self):
        return EmbosserJob.objects.all()


def create_job(request):
    count = EmbosserJob.objects.count()
    job = Job.objects.create(job_number="XXXXX" + str(count + 1), assembly_number="XX", operation_number="XX")
    embosser_job = EmbosserJob.objects.create(job_id="New Job " + str(count + 1))
    embosser_job.has_job_name_been_set = False
    job.full_clean()
    job.save()
    embosser_job.full_clean()
    embosser_job.save()
    return HttpResponseRedirect(reverse('grinder_manager:job_setup', args=(embosser_job.id,)))
#
# def add_field(request, job_id):
#     job = get_object_or_404(Job, pk=job_id)
#     new_field_job = job
#     new_field_name = "Default Name"
#     new_field_text = ""
#     field = Field.objects.create_field(new_field_job, new_field_name, new_field_text, True, True, True, False)
#     job.last_update = timezone.now()
#     job.has_process_outline_been_modified_for_this_operation = True
#     job.full_clean()
#     job.save()
#     return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
