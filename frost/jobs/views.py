import datetime

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
from workcenters.models import WorkCenter, Worker, Operation

from .models import Job, Field, JobInstructions, AssemblyInstructions


class IndexView(generic.ListView):
    template_name = 'jobs/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        workcenter_id = self.kwargs['center_pk']
        workcenter = WorkCenter.objects.get(pk=workcenter_id)
        center_operations = (Operation.objects.all().filter(
                                work_center_id=workcenter)
                                )
        center_timecards = []
        for operation in center_operations.iterator():
            center_timecards.append(operation.timecard_id)
        center_timecards = set(center_timecards)
        center_timecards = list(center_timecards)

        center_operators = []
        for timecard in center_timecards:
            for worker in (Worker.objects.all().filter(
               timecard_id=timecard).iterator()
               ):
                center_operators.append(worker)
        center_operators = set(center_operators)
        center_operators = list(center_operators)

        current_center_operators= []
        for worker in center_operators:
            start = worker.start_time
            end = worker.end_time
            if end == None or (
               start < timezone.make_aware(datetime.datetime(
               2011, 3, 21))
               ) or end > timezone.make_aware(
               datetime.datetime(2011, 3, 22)
               ):
                pass
            else:
                current_center_operators.append(worker)
        current_center_operators = set(current_center_operators)
        current_center_operators = list(current_center_operators)

        current_center_operations = []
        for operator in current_center_operators:
            current_operator_employee_id = operator.employee_id
            for operation in center_operations:
                if operation.employee_id == current_operator_employee_id:
                    if operation.operation_id == 0 and (
                       operation.assembly_id == 0
                       ):
                        pass
                    else:
                        if (operation.end_time == None) or (
                           operation.start_time < operator.start_time
                           ) or (
                           operation.start_time > (
                           operator.start_time + datetime.timedelta(
                                                            days=1))
                           ):
                            pass
                        else:
                            current_center_operations.append(operation)
        current_center_operations = set(current_center_operations)
        current_center_operations = list(current_center_operations)

        current_operation_objects = []
        for operation in current_center_operations:
            real_operation_object = (
                            Job.objects.all().filter(
                            jmojobid=operation.job_id).filter(
                            jmojobassemblyid=operation.assembly_id
                            ).filter(
                            jmojoboperationid=operation.operation_id)
                            )
            current_operation_objects.append(real_operation_object)
        current_operation_objects = set(current_operation_objects)
        current_operation_objects = list(current_operation_objects)

        final_list = []
        for operation in current_operation_objects:
            for object_within in operation.iterator():
                final_list.append(object_within)
        final_list = set(final_list)
        final_list = list(final_list)

        context['jobs'] = final_list
        context['center'] = workcenter_id
        return context

    def get_queryset(self):
        return Job.objects.all()


class PickTemplateView(generic.ListView):
    template_name = 'jobs/pages/pick_template.html'
    model = Job

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = (super(
                    PickTemplateView, self).get_context_data(**kwargs)
                    )
        workcenter = WorkCenter.objects.get(
                        pk=self.kwargs['center_pk']
                        )
        context['processes'] = (Process.objects.all().filter(
                                workcenter=workcenter.workcenter_id)
                                )
        context['uniqueid'] = self.kwargs['urluniqueid']
        context['center'] = self.kwargs['center_pk']
        return context


class PickReopenTemplateView(generic.ListView):
    template_name = 'jobs/pages/pick_reopen_template.html'
    model = Job

    def get_queryset(self):
        return Job.objects.all()

    def get_context_data(self, **kwargs):
        context = (super(
                    PickReopenTemplateView, self
                    ).get_context_data(**kwargs)
                    )
        workcenter = WorkCenter.objects.get(
                                        pk=self.kwargs['center_pk']
                                        )
        context['processes'] = (Process.objects.all().filter(
                                workcenter=workcenter.workcenter_id)
                                )
        context['uniqueid'] = self.kwargs['urluniqueid']
        context['center'] = self.kwargs['center_pk']
        context['submission_number'] = self.kwargs['submission_number']
        return context


class DetailView(generic.DetailView):
    template_name = 'jobs/pages/detail.html'

    def get_object(self, **kwargs):
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        return job

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
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
        context['center'] = self.kwargs['center_pk']
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


class DataView(generic.DetailView):
    template_name = 'jobs/pages/data_view.html'

    def get_object(self, **kwargs):
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        return job

    def get_context_data(self, **kwargs):
        context = super(DataView, self).get_context_data(**kwargs)
        job = Job.objects.get(jmouniqueid=self.kwargs['urluniqueid'])
        jobs = Job.objects.filter(jmojobid=job.jmojobid)
        context['jobs'] = jobs
        context['urluniqueid'] = self.kwargs['urluniqueid']
        context['current_center'] = self.kwargs['center_pk']
        center = WorkCenter.objects.get(pk=self.kwargs['center_pk'])
        context['centers'] = WorkCenter.objects.all().exclude(
                                workcenter_id=center.workcenter_id
                                )
        return context


def save_data(request, center_pk, urluniqueid):
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
            'jobs:detail', args=(center_pk, urluniqueid,))
            )
    if field_to_be_saved.text_is_operator_editable:
        field_to_be_saved.field_text = request.POST.get(
                                                'save_field_text'
                                                )
    if (request.POST.get('save_field_name') == "Default Name"):
        field_to_be_saved.field_has_been_set = False
        field_to_be_saved.editing_mode = True
        messages.error(request, 'Fields require names to be submitted')
        return HttpResponseRedirect(reverse('jobs:detail',
                                            args=(center_pk,
                                            urluniqueid,))
                                            )
    field_to_be_saved.field_has_been_set = True
    field_to_be_saved.editing_mode = False
    field_to_be_saved.full_clean()
    field_to_be_saved.save()
    return HttpResponseRedirect(reverse('jobs:detail',
                                        args=(center_pk,
                                        urluniqueid,))
                                        )

def edit_data(request, center_pk, urluniqueid):
    field_to_be_edited = Field.objects.get(
                                        pk=request.POST['edit_field']
                                        )
    field_to_be_edited.editing_mode = True
    field_to_be_edited.full_clean()
    field_to_be_edited.save()
    return HttpResponseRedirect(reverse('jobs:detail',
                                        args=(center_pk,
                                        urluniqueid,))
                                        )

def add_field(request, center_pk, urluniqueid):
    job = urluniqueid
    new_field_name = "Default Name"
    new_field_text = ""
    submission_number = str(1 + int(
                                Field.objects.all().filter(
                                job=job).filter(
                                field_name="reopens").get(
                                ).field_text)
                                )
    field = Field.objects.create_field(job, new_field_name,
                                       new_field_text, True,
                                       True, True, False, True,
                                       False, submission_number
                                       )
    return HttpResponseRedirect(reverse('jobs:detail', args=(center_pk,
                                                        urluniqueid,))
                                                        )

def delete_field(request, center_pk, urluniqueid):
    field_to_be_deleted = (Field.objects.get(
                                        pk=request.POST['delete_field']
                                        ).delete()
                                        )
    return HttpResponseRedirect(reverse('jobs:detail',
                                        args=(center_pk, urluniqueid,))
                                        )

def set_process_template(request, center_pk, urluniqueid, process_name):
    job = urluniqueid
    process = get_object_or_404(Process, pk=process_name)
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
                                        True, "1"
                                        )
    submit_button_works = Field.objects.create_field(job,
                                        "submit_button_works", "true",
                                        False, False, False, True,
                                        False, True, "1"
                                        )
    number_of_reopens_field = Field.objects.create_field(job,
                                        "reopens", "0", False, False,
                                        False, True, False, True, "1"
                                        )
    return HttpResponseRedirect(reverse('jobs:detail',
                                        args=(center_pk, urluniqueid,))
                                        )

def go_to_detail_or_picker(request, center_pk, urluniqueid):
    for field in Field.objects.all().filter(job=urluniqueid):
        if (field.field_name == "template_set" and
           field.is_a_meta_field == True
           ):
            return HttpResponseRedirect(reverse('jobs:detail',
                                                args=(
                                                center_pk, urluniqueid,))
                                                )
    return HttpResponseRedirect(reverse('jobs:pick_template',
                                        args=(center_pk, urluniqueid,))
                                        )

def submit(request, center_pk, urluniqueid):
    fields = Field.objects.all().filter(job=urluniqueid)
    has_been_submitted = fields.filter(field_name='submitted').get()
    submit_sentinel = (fields.filter(
                                field_name='submit_button_works').get()
                                )
    if submit_sentinel.field_text == "true":
        for field in fields:
            if field.required_for_full_submission == True:
                if (field.field_name == "Default Name" or
                   field.field_text == ""
                   ):
                    messages.error(request,
                                'Required Fields cannot be blank ' +
                                'and must be named')
                    submit_sentinel.field_text == "false"
                    submit_sentinel.full_clean()
                    submit_sentinel.save()
                    return HttpResponseRedirect(reverse('jobs:detail',
                                                args=(center_pk,
                                                    urluniqueid,))
                                                )
            if field.editing_mode == True:
                messages.error(request,
                            'Finish editing fields before submiting'
                            )
                submit_sentinel.field_text == "false"
                submit_sentinel.full_clean()
                submit_sentinel.save()
                return HttpResponseRedirect(reverse('jobs:detail',
                                            args=(center_pk,
                                                urluniqueid,))
                                            )
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
    return HttpResponseRedirect(reverse('jobs:detail', args=(center_pk,
                                                        urluniqueid,))
                                                        )

def reopen(request, center_pk, urluniqueid):
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
        job = urluniqueid
        submission_number = str(1 + int(
                                        Field.objects.all().filter(
                                        job=job
                                        ).filter(
                                        field_name="reopens"
                                        ).get().field_text)
                                        )
    else:
        number_of_reopens = int(number_of_reopens_field.field_text)
        number_of_reopens_field.field_text = str(number_of_reopens)
        number_of_reopens_field.full_clean()
        number_of_reopens_field.save()
        job = urluniqueid
        submission_number = str(1 + int(
                                        Field.objects.all().filter(
                                        job=job
                                        ).filter(
                                        field_name="reopens"
                                        ).get().field_text)
                                        )
    return HttpResponseRedirect(reverse('jobs:reopen_template',
                                args=(center_pk, urluniqueid,
                                        submission_number))
                                )

def set_reopen_template(request, center_pk, urluniqueid,
   process_name, submission_number
   ):
    job = urluniqueid
    process = get_object_or_404(Process, pk=process_name)
    for field in process.outlinefield_set.all():
        new_field = Field.objects.create_field(job,
                            field.OUTLINE_field_name,
                            field.OUTLINE_field_text,
                            field.OUTLINE_name_is_operator_editable,
                            field.OUTLINE_text_is_operator_editable,
                            field.OUTLINE_required_for_full_submission,
                            True, field.OUTLINE_can_be_deleted, False,
                            submission_number
                            )
    return HttpResponseRedirect(reverse('jobs:detail',
                                args=(center_pk, urluniqueid,))
                                )

class ManagerIndex(generic.ListView):
    template_name = 'jobs/pages/manager_index.html'

    def get_queryset(self):
        search_query = self.request.GET.get('search_box', '')
        return Job.objects.all().filter(jmojobid__icontains=search_query)

    def get_context_data(self, **kwargs):
        context = super(ManagerIndex, self).get_context_data(**kwargs)
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


class ManagerDataView(generic.DetailView):
    template_name = 'jobs/pages/manager_data_view.html'

    def get_object(self, **kwargs):
        job = Job.objects.all()
        return job

    def get_context_data(self, **kwargs):
        context = super(ManagerDataView, self).get_context_data(**kwargs)
        context['job'] = self.kwargs['jobid']
        return context

class ManagerCreateReport(generic.DetailView):
    template_name = 'jobs/pages/manager_create_report.html'

    def get_object(self, **kwargs):
        job = Job.objects.all()
        return job

    def get_context_data(self, **kwargs):
        context = super(ManagerCreateReport, self).get_context_data(**kwargs)
        context['job'] = self.kwargs['jobid']
        context['report'] = True
        return context

def populate(request, jobid):
    fields = []
    for item in request.POST:
        if "field" not in str(item):
            pass
        else:
            fields.append(request.POST[item])
    print(fields)
    return HttpResponseRedirect(reverse('jobs:manager_index'))

class JobReport(generic.DetailView):
    template_name = 'jobs/pages/job_report.html'

    def get_object(self, **kwargs):
        job = Job.objects.all()
        return job

    def get_context_data(self, **kwargs):
        context = super(JobReport, self).get_context_data(**kwargs)
        context['job'] = self.kwargs['jobid']
        return context
