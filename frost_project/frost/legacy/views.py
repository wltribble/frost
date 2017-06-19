from django.shortcuts import render
from django.views import generic

from .models import Joboperations as OldJob

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'legacy/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['jobs'] = OldJob.objects.all()
        for job in OldJob.objects.all():
            try:
                context['incomplete_jobs'].append(job)
            except:
                context['incomplete_jobs'] = []
                context['incomplete_jobs'].append(job)
        return context

    def get_queryset(self):
        return OldJob.objects.all()