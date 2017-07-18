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

from .models import Job, Field, JobInstructions, AssemblyInstructions, Notes


class IndexView(generic.ListView):
    template_name = 'jobs/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        search_query = self.request.GET.get('search_box', 'xxxxxxxxxxxxxxxxxxxx')
        workcenter_id = self.kwargs['center_pk']
        workcenter = WorkCenter.objects.get(pk=workcenter_id)
        center_operations = (Operation.objects.all().filter(
                            work_center_id=workcenter).filter(
                            start_time__gte=(datetime.datetime.now()
                                            - datetime.timedelta(hours=12))
                            ).filter(
                            end_time=None
                            ))

        final_list = []
        for operation in center_operations.iterator():
            if str(operation.assembly_id) == "0" and str(operation.operation_id) == "0":
                pass
            else:
                real_operation_object = (
                                Job.objects.filter(jmoclosed=0).filter(
                                jmojobid=operation.job_id).filter(
                                jmojobassemblyid=operation.assembly_id
                                ).filter(
                                jmojoboperationid=operation.operation_id
                                ).get()
                                )
                final_list.append(real_operation_object)

        final_list = set(final_list)
        final_list = list(final_list)
        final_list.sort(key=lambda x: x.jmoduedate, reverse=True)

        context['jobs'] = final_list
        context['center'] = workcenter_id


        old_center_operations = (Operation.objects.all().filter(
                            work_center_id=workcenter).filter(
                            start_time__lte=(datetime.datetime.now())
                            ).exclude(
                            end_time=None
                            ))

        intermediate_old_op_list = []
        for operation in old_center_operations.iterator():
            if str(operation.assembly_id) == "0" and str(operation.operation_id) == "0":
                pass
            else:
                try:
                    real_old_operation_object = (
                                Job.objects.all().filter(
                                jmojobid=operation.job_id).filter(
                                jmojobassemblyid=operation.assembly_id
                                ).filter(
                                jmojoboperationid=operation.operation_id
                                ).get()
                                )
                    intermediate_old_op_list.append(real_old_operation_object)
                except:
                    pass

        intermediate_old_op_list = set(intermediate_old_op_list)
        intermediate_old_op_list = list(intermediate_old_op_list)
        intermediate_old_op_list.sort(key=lambda x: x.jmoduedate, reverse=True)

        final_old_op_list = []
        counter = 0
        for op in intermediate_old_op_list:
            if counter < 10:
                if search_query in op.jmojobid or search_query in str(op.jmojobassemblyid) or search_query in str(op.jmojoboperationid):
                    final_old_op_list.append(op)
                    counter += 1
                else:
                    pass
            else:
                break
        context['history'] = final_old_op_list
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
                                ).filter(operator_template=True)
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
                                workcenter=workcenter.workcenter_id
                                ).filter(operator_template=True)
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
                                    range(0, 2 + int(
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
        context['notes'] = Notes.objects.all().filter(job=job.jmouniqueid).get()
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
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
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
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
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
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
    return HttpResponseRedirect(reverse('jobs:detail', args=(center_pk,
                                                        urluniqueid,))
                                                        )

def delete_field(request, center_pk, urluniqueid):
    field_to_be_deleted = (Field.objects.get(
                                        pk=request.POST['delete_field']
                                        ).delete()
                                        )
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
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
    try:
        notes = Notes.objects.get(job=urluniqueid)
    except:
        notes = Notes.objects.create(job=urluniqueid, text="")
    return HttpResponseRedirect(reverse('jobs:detail',
                                        args=(center_pk, urluniqueid,))
                                        )

def go_to_detail_or_picker(request, center_pk, urluniqueid):
    if center_pk == "1":
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
    else:
        job = ((Job.objects.get(jmouniqueid=urluniqueid)).jmojobid).strip()
        return HttpResponseRedirect(reverse('workcenters:manager_data_view'), args=(job,))

def submit(request, center_pk, urluniqueid):
    fields = Field.objects.all().filter(job=urluniqueid)
    has_been_submitted = fields.filter(field_name='submitted').get()
    submit_sentinel = (fields.filter(
                                field_name='submit_button_works').get()
                                )
    fields_that_need_to_be_checked = Field.objects.all().filter(
                                                    job=urluniqueid
                                                    ).filter(
                                                    is_a_meta_field=False
                                                    )
    if submit_sentinel.field_text == "true":
        for field in fields_that_need_to_be_checked:
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
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
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
    note_to_be_saved = Notes.objects.get(job=urluniqueid)
    note_to_be_saved.text = request.POST.get('notes')
    note_to_be_saved.full_clean()
    note_to_be_saved.save()
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


class ManagerDataView(generic.DetailView):
    template_name = 'jobs/pages/manager_data_view.html'

    def get_object(self, **kwargs):
        job = Job.objects.all().order_by('jmojoboperationid')
        return job

    def get_context_data(self, **kwargs):
        context = super(ManagerDataView, self).get_context_data(**kwargs)
        context['job'] = self.kwargs['jobid']
        return context

class ManagerCreateReport(generic.DetailView):
    template_name = 'jobs/pages/manager_create_report.html'

    def get_object(self, **kwargs):
        job = Job.objects.all().order_by('jmojoboperationid')
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
    return HttpResponseRedirect(reverse('jobs:manager_index'))


class JobReport(generic.DetailView):
    template_name = 'jobs/pages/job_report.html'

    def get_object(self, **kwargs):
        job = Job.objects.all().order_by('jmojoboperationid')
        return job

    def get_context_data(self, **kwargs):
        context = super(JobReport, self).get_context_data(**kwargs)
        context['job'] = self.kwargs['jobid']

        fields = []
        for item in self.request.GET:
            if "field" not in str(item):
                pass
            else:
                get_item = self.request.GET[item]
                fields.append(get_item)
        context['fields'] = fields

        return context
