from django.http import HttpResponseRedirect
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse
from django.views import generic

from .models import WorkCenter, Worker, Operation
# Create your views here.

class PickCenterView(generic.ListView):
    template_name = 'jobs/pages/pick_center.html'
    model = WorkCenter

    def get_queryset(self):
        return WorkCenter.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PickCenterView, self).get_context_data(**kwargs)
        context['workcenters'] = WorkCenter.objects.all()
        return context