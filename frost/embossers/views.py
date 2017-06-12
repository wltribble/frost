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
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.all()


class PickTemplateView(generic.ListView):
    template_name = 'embossers/pages/pick_template.html'
    model = Job

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickTemplateView, self).get_context_data(**kwargs)
        context['processes'] = Process.objects.all()
        context['job'] = Job.objects.get(id=self.kwargs.get('job_id'))
        return context



class DetailView(generic.DetailView):
    model = Job
    template_name = 'embossers/pages/detail.html'

    def get_queryset(self):
        return Job.objects.all()

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
        field_to_be_saved.full_clean()
        field_to_be_saved.save()
        job.full_clean()
        job.save()
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    except:
        return HttpResponseRedirect(reverse('embossers:index'))

def edit_data(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    try:
        field_to_be_edited = job.field_set.get(pk=request.POST['edit_field'])
        field_to_be_edited.editing_mode = True
        field_to_be_edited.full_clean()
        field_to_be_edited.save()
        job.last_update = timezone.now()
        job.full_clean()
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
        field = Field.objects.create_field(new_field_job, new_field_name, new_field_text, True, True, True, False)
        job.last_update = timezone.now()
        job.has_process_outline_been_modified_for_this_operation = True
        job.full_clean()
        job.save()
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
    except:
        return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))

def delete_field(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    field_to_be_deleted = job.field_set.get(pk=request.POST['delete_field']).delete()
    job.last_update = timezone.now()
    job.has_process_outline_been_modified_for_this_operation = True
    job.save()
    return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))

def set_process_template(request, job_id, process_name):
    job = get_object_or_404(Job, pk=job_id)
    process = get_object_or_404(Process, pk=process_name)
    job.process_outline = process.process_name
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job, field.OUTLINE_field_name, field.OUTLINE_field_text, field.OUTLINE_name_is_operator_editable, field.OUTLINE_text_is_operator_editable, field.OUTLINE_required_for_full_submission, True)
    job.last_update = timezone.now()
    job.full_clean()
    job.save()
    return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))

def create_job(request):
    count = Job.objects.count()
    job = Job.objects.create(job_id="New Job " + str(count + 1))
    return HttpResponseRedirect(reverse('embossers:pick_template', args=(job.id,)))

def set_job_name(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    job_number = request.POST['job_number_text_box']
    assembly_number = request.POST['assembly_number_text_box']
    operation_number = request.POST['operation_number_text_box']
    if job_number != "" and assembly_number != "" and operation_number != "":
        job.job_id = job_number + "-" + assembly_number + "-" + operation_number
        job.hase_job_name_been_set = True
        job.last_update = timezone.now()
        job.full_clean()
        job.save()
    return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))

def submit(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    completed = True
    for field in job.field_set.all():
        field.name_is_operator_editable = False
        field.text_is_operator_editable = False
        field.full_clean()
        field.save()
    # job.date_submitted = timezone.now()
    job.full_clean()
    job.save()
    return HttpResponseRedirect(reverse('embossers:detail', args=(job.id,)))
