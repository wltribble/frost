import uuid

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

from .models import Job, Field


class IndexView(generic.ListView):
    template_name = 'jobs/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        for job in context['jobs']:
            try:
                context['current_jobs'].append(job)
            except:
                context['current_jobs'] = []
                context['current_jobs'].append(job)
        return context

    def get_queryset(self):
        return Job.objects.all()


class PickTemplateView(generic.ListView):
    template_name = 'jobs/pages/pick_template.html'
    model = Job

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickTemplateView, self).get_context_data(**kwargs)
        context['processes'] = Process.objects.all()
        context['uniqueid'] = self.kwargs['urluniqueid']
        return context


class DetailView(generic.DetailView):
    template_name = 'jobs/pages/detail.html'

    def get_object(self, **kwargs):
        for job_iterator in Job.objects.raw('SELECT * FROM JobOperations WHERE [jmouniqueid] = %s', [self.kwargs['urluniqueid']]):
            job = job_iterator
        return job

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        for job_iterator in Job.objects.raw('SELECT * FROM JobOperations WHERE [jmouniqueid] = %s', [self.kwargs['urluniqueid']]):
            context['job'] = job_iterator
        context['fields'] = Field.objects.all().filter(job=self.kwargs['urluniqueid'])
        context['urluniqueid'] = self.kwargs['urluniqueid']
        return context


def save_data(request, urluniqueid):
    field_to_be_saved = Field.objects.get(pk=request.POST['save_field'])
    if field_to_be_saved.name_is_operator_editable and request.POST.get('save_field_name') != "":
        field_to_be_saved.field_name = request.POST.get('save_field_name')
    if field_to_be_saved.name_is_operator_editable and request.POST.get('save_field_name') == "":
        messages.error(request, 'Fields require names to be submitted')
        return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
    if field_to_be_saved.text_is_operator_editable:
        field_to_be_saved.field_text = request.POST.get('save_field_text')
    if (request.POST.get('save_field_name') == "Default Name"):
        field_to_be_saved.field_has_been_set = False
        field_to_be_saved.editing_mode = True
        messages.error(request, 'Fields require names to be submitted')
        return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
    field_to_be_saved.field_has_been_set = True
    field_to_be_saved.editing_mode = False
    field_to_be_saved.full_clean()
    field_to_be_saved.save()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def edit_data(request, urluniqueid):
    field_to_be_edited = Field.objects.get(pk=request.POST['edit_field'])
    field_to_be_edited.editing_mode = True
    field_to_be_edited.full_clean()
    field_to_be_edited.save()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def add_field(request, urluniqueid):
    job = urluniqueid
    new_field_name = "Default Name"
    new_field_text = ""
    field = Field.objects.create_field(job, new_field_name, new_field_text, True, True, True, False, True, False)
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def delete_field(request, urluniqueid):
    field_to_be_deleted = Field.objects.get(pk=request.POST['delete_field']).delete()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def set_process_template(request, urluniqueid, process_name):
    job = urluniqueid
    process = get_object_or_404(Process, pk=process_name)
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job, field.OUTLINE_field_name, field.OUTLINE_field_text, field.OUTLINE_name_is_operator_editable, field.OUTLINE_text_is_operator_editable, field.OUTLINE_required_for_full_submission, True, field.OUTLINE_can_be_deleted, False)
    job_template_has_now_been_set = Field.objects.create_field(job, "template_set", process_name, False, False, False, True, False, True)
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def go_to_detail_or_picker(request, urluniqueid):
    for field in Field.objects.all().filter(job=urluniqueid):
        print (field.field_name)
        if field.field_name == "template_set" and field.is_a_meta_field == True:
            print ('found')
            return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
    return HttpResponseRedirect(reverse('jobs:pick_template', args=(urluniqueid,)))
# def submit(request, jmouniqueid):
#     job = get_object_or_404(Job, pk=jmouniqueid)
#     fields = job.field_set.all()
#     if job.has_job_name_been_set == False:
#         messages.error(request, 'Job ID must be set before submiting')
#         job.disable_submit_button = True
#     elif job.disable_submit_button == False:
#         for field in fields:
#             if field.required_for_full_submission == True:
#                 if field.field_name == "Default Name" or field.field_text == "":
#                     messages.error(request, 'Required Fields cannot be blank and must be named')
#                     job.disable_submit_button = True
#             if field.editing_mode == True:
#                 messages.error(request, 'Finish editing fields before submiting')
#                 job.disable_submit_button = True
#     if job.disable_submit_button == False:
#         job.completed = True
#         for field in fields:
#             field.name_is_operator_editable = False
#             field.text_is_operator_editable = False
#             field.full_clean()
#             field.save()
#         job.date_submitted = timezone.now()
#     else:
#         job.disable_submit_button = False
#     job.full_clean()
#     job.save()
#     return HttpResponseRedirect(reverse('jobs:detail', args=(job.id,)))
