from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.db import migrations

from processes.models import Process

from .models import Job, Field


class IndexView(generic.ListView):
    template_name = 'embossers/pages/index.html'
    context_object_name = 'latest_job_list'

    def get_queryset(self):
        """Return the last 5 created jobs (not including those
        set to be created in the future)."""
        return Job.objects.filter(
            date_created__lte=timezone.now()
        ).order_by('-date_created')[:5]


class PickTemplateView(generic.ListView):
    model = Process
    context_object_name = 'latest_process_list'
    template_name = 'embossers/pages/pick_template.html'

    def get_queryset(self):
        return Process.objects.all().order_by('-process_date_created')


class DetailView(generic.DetailView):
    model = Job
    template_name = 'embossers/pages/detail.html'

    def get_queryset(self):
        return Job.objects.filter(date_created__lte=timezone.now())

def save_data(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    try:
        field_to_be_saved = job.field_set.get(pk=request.POST['save_field'])
        if field_to_be_saved.name_is_operator_editable:
            field_to_be_saved.field_name = request.POST.get('save_field_name')
        if field_to_be_saved.text_is_operator_editable:
            field_to_be_saved.field_text = request.POST.get('save_field_text')
        if (request.POST.get('save_field_name') == "Default Name") or (request.POST.get('save_field_text') == ""):
            field_to_be_saved.field_has_been_set = False
            field_to_be_saved.editing_mode = True
        else:
            field_to_be_saved.field_has_been_set = True
            field_to_be_saved.editing_mode = False
            job.last_update = timezone.now()
        field_to_be_saved.save()
        job.save()
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    except:
        return HttpResponseRedirect(reverse('embossers:index'))

def edit_data(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    try:
        field_to_be_edited = job.field_set.get(pk=request.POST['edit_field'])
        field_to_be_edited.editing_mode = True
        field_to_be_edited.save()
        job.last_update = timezone.now()
        job.save()
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    except:
        return HttpResponseRedirect(reverse('embossers:index'))

def add_field(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    new_field_job = job
    try:
        new_field_name = "Default Name"
        new_field_text = ""
        field = Field.objects.create_field(new_field_job, new_field_name, new_field_text)
        job.last_update = timezone.now()
        if job.process_outline != "None":
            job.has_process_outline_been_modified_for_this_operation = True
        job.save()
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    except:
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))

def delete_field(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    field_to_be_deleted = job.field_set.get(pk=request.POST['delete_field']).delete()
    job.last_update = timezone.now()
    if job.process_outline != "None":
        job.has_process_outline_been_modified_for_this_operation = True
    job.save()
    return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
