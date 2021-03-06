from django.conf.urls import url, include

from jobs.views import ManagerIndex, ManagerDataView, ManagerCreateReport, populate, JobReport

from .views import PickCenterView, EngineeringIndexView, EngineeringDetailView, EngineeringPickOperationView, EngineeringDataView, engineering_save_data, engineering_edit_data, engineering_add_field, engineering_delete_field, PickEngineeringProcessView, set_process_template, release_to_operator, go_to_detail_or_picker


app_name = 'workcenters'
urlpatterns = [
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/create_report/$', ManagerCreateReport.as_view(), name='create_report'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/populate/$', populate, name='populate_report'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/report/$', JobReport.as_view(), name='job_report'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/$', ManagerDataView.as_view(), name='manager_data_view'),
    url(r'^manager/$', ManagerIndex.as_view(), name='manager_index'),
    url(r'^engineering/(?P<jobid>[0-9a-zA-Z-]+)/pick_operation/$', EngineeringPickOperationView.as_view(), name='engineering_pick_operation'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/data/$', EngineeringDataView.as_view(), name='engineering_data_view'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/save/$', engineering_save_data, name='engineering_save_data'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/decide/$', go_to_detail_or_picker, name='go_to_detail_or_picker'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/edit/$', engineering_edit_data, name='engineering_edit_data'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/add/$', engineering_add_field, name='engineering_add_field'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/delete/$', engineering_delete_field, name='engineering_delete_field'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/pick_process/$', PickEngineeringProcessView.as_view(), name='pick_process_template'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/set/(?P<process_name>[0-9]+)/$', set_process_template, name='set_process_template'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/release_to_operator/$', release_to_operator, name='release_to_operator'),
    url(r'^engineering/(?P<urluniqueid>[0-9a-fA-F-]+)/$', EngineeringDetailView.as_view(), name='engineering_detail'),
    url(r'^engineering/$', EngineeringIndexView.as_view(), name='engineering_index'),
    url(r'^', PickCenterView.as_view(), name='pick_center'),
]
