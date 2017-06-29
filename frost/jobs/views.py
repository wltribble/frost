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
        context['fields'] = Field.objects.all().filter(job=self.kwargs['urluniqueid']).filter(is_a_meta_field=False)
        context['urluniqueid'] = self.kwargs['urluniqueid']
        context['metafields'] = Field.objects.all().filter(job=self.kwargs['urluniqueid']).filter(is_a_meta_field=True)
        context['reopen_number'] = range(0, 1 + int(Field.objects.all().filter(job=self.kwargs['urluniqueid']).filter(field_name="reopens").get().field_text))
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
    submission_number = str(1 + int(Field.objects.all().filter(job=self.kwargs['urluniqueid']).filter(field_name="reopens").get().field_text))
    field = Field.objects.create_field(job, new_field_name, new_field_text, True, True, True, False, True, False, submission_number)
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def delete_field(request, urluniqueid):
    field_to_be_deleted = Field.objects.get(pk=request.POST['delete_field']).delete()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def set_process_template(request, urluniqueid, process_name):
    job = urluniqueid
    process = get_object_or_404(Process, pk=process_name)
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job, field.OUTLINE_field_name, field.OUTLINE_field_text, field.OUTLINE_name_is_operator_editable, field.OUTLINE_text_is_operator_editable, field.OUTLINE_required_for_full_submission, True, field.OUTLINE_can_be_deleted, False, "1")
    job_template_has_now_been_set = Field.objects.create_field(job, "template_set", process.process_name, False, False, False, True, False, True, "0")
    job_has_been_submitted_boolean = Field.objects.create_field(job, "submitted", "false", False, False, False, True, False, True, "0")
    submit_button_works = Field.objects.create_field(job, "submit_button_works", "true", False, False, False, True, False, True, "0")
    number_of_reopens_field = Field.objects.create_field(job, "reopens", "0", False, False, False, True, False, True, "0")
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def go_to_detail_or_picker(request, urluniqueid):
    for field in Field.objects.all().filter(job=urluniqueid):
        print (field.field_name)
        if field.field_name == "template_set" and field.is_a_meta_field == True:
            print ('found')
            return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
    return HttpResponseRedirect(reverse('jobs:pick_template', args=(urluniqueid,)))

def submit(request, urluniqueid):
    fields = Field.objects.all().filter(job=urluniqueid)
    has_been_submitted = fields.filter(field_name='submitted').get()
    submit_sentinel = fields.filter(field_name='submit_button_works').get()

    if submit_sentinel.field_text == "true":
        for field in fields:
            if field.required_for_full_submission == True:
                if field.field_name == "Default Name" or field.field_text == "":
                    messages.error(request, 'Required Fields cannot be blank and must be named')
                    submit_sentinel.field_text == "false"
                    submit_sentinel.full_clean()
                    submit_sentinel.save()
                    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
            if field.editing_mode == True:
                messages.error(request, 'Finish editing fields before submiting')
                submit_sentinel.field_text == "false"
                submit_sentinel.full_clean()
                submit_sentinel.save()
                return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
    if submit_sentinel.field_text == "true":
        has_been_submitted.field_text = "true"
        has_been_submitted.full_clean()
        has_been_submitted.save()
        for field in fields:
            if field.is_a_meta_field == False:
                field.name_is_operator_editable = False
                field.text_is_operator_editable = False
                field.full_clean()
                field.save()
    else:
        submit_sentinel.field_text == "true"
        submit_sentinel.full_clean()
        submit_sentinel.save()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))

def reopen(request, urluniqueid):
    fields = Field.objects.all().filter(job=urluniqueid)
    has_been_submitted = fields.filter(field_name='submitted').get()
    number_of_reopens_field = fields.filter(field_name='reopens').get()

    if has_been_submitted.field_text == "true":
        has_been_submitted.field_text = "false"
        has_been_submitted.full_clean()
        has_been_submitted.save()

        number_of_reopens = int(number_of_reopens_field.field_text)
        number_of_reopens += 1
        number_of_reopens_field.field_text = str(number_of_reopens)
        number_of_reopens_field.full_clean()
        number_of_reopens_field.save()
    return HttpResponseRedirect(reverse('jobs:detail', args=(urluniqueid,)))
