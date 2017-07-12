from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic

from jobs.models import Job, JobInstructions, AssemblyInstructions, Field

from .models import WorkCenter, Worker, Operation
# Create your views here.

class PickCenterView(generic.ListView):
    template_name = 'jobs/pages/pick_center.html'
    model = WorkCenter

    def get_queryset(self):
        return WorkCenter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickCenterView, self).get_context_data(**kwargs)
        context['workcenters'] = WorkCenter.objects.all().exclude(
                                                            workcenter_id='ENG'
                                                            ).order_by(
                                                                'workcenter_id'
                                                            )
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
        context['reopen_number'] = (
                                    range(1, 2 + int(
                                    Field.objects.all().filter(
                                    job=self.kwargs['urluniqueid']
                                    ).filter(
                                    field_name="reopens"
                                    ).get().field_text))
                                    )
        context['center'] = job.jmoworkcenterid
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
    submission_number = str(1)
    field = Field.objects.create_field(job, new_field_name,
                                       new_field_text, True,
                                       True, True, False, True,
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


def release_to_operator(request, urluniqueid):
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
                    return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                                args=(urluniqueid,))
                                                )
            if field.editing_mode == True:
                messages.error(request,
                            'Finish editing fields before submiting'
                            )
                submit_sentinel.field_text == "false"
                submit_sentinel.full_clean()
                submit_sentinel.save()
                return HttpResponseRedirect(reverse('workcenters:engineering_detail',
                                            args=(urluniqueid,))
                                            )
    if submit_sentinel.field_text == "true":
        has_been_submitted.field_text = "false"
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
    return HttpResponseRedirect(reverse('workcenters:engineering_detail', args=(urluniqueid,))
                                                        )
