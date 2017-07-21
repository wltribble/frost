from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages

from jobs.models import Job, JobInstructions, AssemblyInstructions, Field
from processes.models import Process

from .models import WorkCenter, Worker, Operation
# Create your views here.

class PickCenterView(generic.ListView):
    template_name = 'jobs/pages/pick_center.html'
    model = WorkCenter

    def get_queryset(self):
        return WorkCenter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickCenterView, self).get_context_data(**kwargs)
        workcenters = WorkCenter.objects.all().exclude(
                                        workcenter_id='ENG'
                                        ).order_by(
                                            'workcenter_id'
                                        )
        workcenter_ids = []
        for workcenter in workcenters:
            workcenter_ids.append(str(workcenter.workcenter_id))
        context['workcenters'] = workcenter_ids

        employees = {}
        operations = Operation.objects.exclude(active=0)
        for operation in operations:
            employees[str(operation.employee_id)] = str(operation.work_center_id)
        context['employees'] = employees
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
        context = super(EngineeringPickOperationView, self).get_context_data(
                                                                    **kwargs
                                                                    )
        job = self.kwargs['jobid']
        jobs = Job.objects.all().filter(jmojobid__icontains=job).order_by(
                                                        'jmojoboperationid'
                                                        )
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


        context['center'] = job.jmoworkcenterid
        context['reopen_number'] = "0"
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


class EngineeringDataView(generic.DetailView):
    template_name = 'jobs/pages/engineering_data_view.html'

    def get_object(self, **kwargs):
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        return job

    def get_context_data(self, **kwargs):
        context = super(EngineeringDataView, self).get_context_data(**kwargs)
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        jobs = Job.objects.filter(jmojobid=job.jmojobid)
        context['jobs'] = jobs
        context['urluniqueid'] = self.kwargs['urluniqueid']
        context['centers'] = WorkCenter.objects.all()
        return context


def engineering_save_data(request, urluniqueid):
    field_to_be_saved = Field.objects.get(
                        pk=request.POST['save_field']
                        )
    if (field_to_be_saved.name_is_operator_editable and
       request.POST.get('save_field_name') != ""):
        field_to_be_saved.field_name = request.POST.get(
                                        'save_field_name'
                                        )
    if (field_to_be_saved.name_is_operator_editable and
       request.POST.get('save_field_name') == ""):
        messages.error(request, 'Fields require names to be submitted')
        return HttpResponseRedirect(reverse(
            'workcenters:engineering_detail', args=(urluniqueid,))
            )
    if field_to_be_saved.text_is_operator_editable:
        field_to_be_saved.field_text = request.POST.get(
                                                'save_field_text'
                                                )
    if (request.POST.get('save_field_name') == "Default Name"):
        field_to_be_saved.field_has_been_set = False
        field_to_be_saved.editing_mode = True
        messages.error(request, 'Fields require names to be submitted')
        return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                            args=(urluniqueid,))
                                            )
    field_to_be_saved.field_has_been_set = True
    field_to_be_saved.editing_mode = False
    field_to_be_saved.full_clean()
    field_to_be_saved.save()
    return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                        args=(urluniqueid,))
                                        )

def engineering_edit_data(request, urluniqueid):
    field_to_be_edited = Field.objects.get(
                                        pk=request.POST['edit_field']
                                        )
    field_to_be_edited.editing_mode = True
    field_to_be_edited.full_clean()
    field_to_be_edited.save()
    return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                        args=(urluniqueid,))
                                        )

def engineering_add_field(request, urluniqueid):
    job = urluniqueid
    new_field_name = "Default Name"
    new_field_text = ""
    submission_number = str(0)
    field = Field.objects.create_field(job, new_field_name,
                                       new_field_text, True,
                                       True, False, False, True,
                                       False, submission_number
                                       )
    return HttpResponseRedirect(reverse('workcenters:engineering_detail', args=(urluniqueid,))
                                                        )

def engineering_delete_field(request, urluniqueid):
    field_to_be_deleted = (Field.objects.get(
                                        pk=request.POST['delete_field']
                                        ).delete()
                                        )
    return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                        args=(urluniqueid,))
                                        )


class PickEngineeringProcessView(generic.ListView):
    template_name = 'jobs/pages/pick_engineering_template.html'
    model = Job

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = (super(
                    PickEngineeringProcessView, self
                    ).get_context_data(**kwargs)
                    )
        job = Job.objects.all().filter(jmouniqueid=self.kwargs['urluniqueid']).get()
        context['processes'] = (Process.objects.all().filter(
                                workcenter=job.jmoworkcenterid
                                ).filter(operator_template=False)
                                )
        context['uniqueid'] = self.kwargs['urluniqueid']
        return context


def set_process_template(request, urluniqueid, process_name):
    job = urluniqueid
    job_object = Job.objects.get(jmouniqueid=job)
    workcenter = job_object.jmoworkcenterid
    process = get_object_or_404(Process, pk=process_name)
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job,
                            field.OUTLINE_field_name,
                            field.OUTLINE_field_text,
                            field.OUTLINE_name_is_operator_editable,
                            field.OUTLINE_text_is_operator_editable,
                            field.OUTLINE_required_for_full_submission,
                            True, field.OUTLINE_can_be_deleted,
                            False, "0"
                            )

    job_has_been_released_boolean = Field.objects.create_field(job,
                                        "released", "true", False,
                                        False, False, True, False,
                                        True, "0"
                                        )
    release_button_works = Field.objects.create_field(job,
                                        "release_button_works", "true",
                                        False, False, False, True,
                                        False, True, "0"
                                        )

    operator_process = Process.objects.filter(workcenter=workcenter).filter(process_name=process.process_name).filter(operator_template=True).get()
    process = operator_process
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job,
                            field.OUTLINE_field_name,
                            field.OUTLINE_field_text,
                            field.OUTLINE_name_is_operator_editable,
                            field.OUTLINE_text_is_operator_editable,
                            field.OUTLINE_required_for_full_submission,
                            True, field.OUTLINE_can_be_deleted,
                            False, "1"
                            )
    job_template_has_now_been_set = Field.objects.create_field(
                                        job, "template_set",
                                        process.process_name, False,
                                        False, False, True, False,
                                        True, "1"
                                        )
    job_has_been_submitted_boolean = Field.objects.create_field(job,
                                        "submitted", "false", False,
                                        False, False, True, False,
                                        True, "0"
                                        )
    try:
        submit_button_works = Field.objects.get(field_name="submit_button_works")
        submit_button_works.field_text = "true"
    except:
        submit_button_works = Field.objects.create_field(job,
                                            "submit_button_works", "true",
                                            False, False, False, True,
                                            False, True, "0"
                                            )
    try:
        number_of_reopens_field = Field.objects.get(field_name="reopens")
        number_of_reopens_field = Field.objects.get(field_name="0")
    except:
        number_of_reopens_field = Field.objects.create_field(job,
                                            "reopens", "0", False, False,
                                            False, True, False, True, "1"
                                            )


    return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                        args=(urluniqueid,))
                                        )

def go_to_detail_or_picker(request, urluniqueid):
    for field in Field.objects.all().filter(job=urluniqueid):
        if (field.field_name == "template_set" and
           field.is_a_meta_field == True
           ):
            return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                                args=(
                                                urluniqueid,))
                                                )
    return HttpResponseRedirect(reverse('workcenters:pick_process_template',
                                        args=(urluniqueid,))
                                        )


def release_to_operator(request, urluniqueid):
    fields = Field.objects.all().filter(job=urluniqueid).filter(submission_number="0")
    has_been_released = fields.filter(field_name='released').get()
    release_sentinel = (fields.filter(
                                field_name='release_button_works').get()
                                )
    if release_sentinel.field_text == "true":
        for field in fields:
            if (field.field_name == "Default Name" or
               field.field_text == ""
               ):
                messages.error(request,
                            'Required Fields cannot be blank')
                release_sentinel.field_text == "false"
                release_sentinel.full_clean()
                release_sentinel.save()
                return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                            args=(urluniqueid,))
                                            )
            if field.editing_mode == True:
                messages.error(request,
                            'Finish editing fields before submiting'
                            )
                release_sentinel.field_text == "false"
                release_sentinel.full_clean()
                release_sentinel.save()
                return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                            args=(urluniqueid,))
                                            )
    if release_sentinel.field_text == "true":
        has_been_released.field_text = "true"
        has_been_released.full_clean()
        has_been_released.save()
        for field in fields:
            if field.is_a_meta_field == False:
                field.name_is_operator_editable = False
                field.text_is_operator_editable = False
                field.full_clean()
                field.save()
    else:
        release_sentinel.field_text == "true"
        release_sentinel.full_clean()
        release_sentinel.save()
    return HttpResponseRedirect(reverse('workcenters:engineering_detail', args=(urluniqueid,)))
