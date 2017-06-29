from django.conf.urls import url

from .views import PickCenterView


app_name = 'workcenters'
urlpatterns = [
    url(r'^$', PickCenterView.as_view(), name='pick_center'),
    url(r'^(?P<center_pk>[0-9]+/jobs/$', include('jobs.urls', namespace='jobs')),
]
