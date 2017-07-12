from django.conf.urls import url, include

from .views import PickCenterView, ManagerIndex, ManagerDataView, ManagerCreateReport, populate, JobReport


app_name = 'workcenters'
urlpatterns = [
    url(r'^', PickCenterView.as_view(), name='pick_center'),
    url(r'^manager/$', ManagerIndex.as_view(), name='manager_index'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/$', ManagerDataView.as_view(), name='manager_data_view'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/create_report/$', ManagerCreateReport.as_view(), name='create_report'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/populate/$', populate, name='populate_report'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/report/$', JobReport.as_view(), name='job_report'),
]
