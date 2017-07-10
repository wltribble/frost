from django.conf.urls import url

from .views import IndexView, DetailView, PickTemplateView, save_data, edit_data, add_field, delete_field, set_process_template, go_to_detail_or_picker, submit, reopen, PickReopenTemplateView, set_reopen_template, DataView, ManagerIndex, ManagerDataView, ManagerCreateReport

app_name = 'jobs'
urlpatterns = [
    url(r'^(?P<center_pk>[0-9]+)/$', IndexView.as_view(), name='index'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/$', PickTemplateView.as_view(), name='pick_template'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/save/$', save_data, name='save_data'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/edit/$', edit_data, name='edit_data'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/add/$', add_field, name='add_field'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/delete/$', delete_field, name='delete_field'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/set/(?P<process_name>[0-9]+)/$', set_process_template, name='set_process_template'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/decide/$', go_to_detail_or_picker, name='go_to_detail_or_picker'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/submit/$', submit, name='submit'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/reopen/$', reopen, name='reopen'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/reopen/(?P<submission_number>[0-9]+)/$', PickReopenTemplateView.as_view(), name='reopen_template'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/reopen/(?P<submission_number>[0-9]+)/set/(?P<process_name>[0-9]+)/$', set_reopen_template, name='set_reopen_template'),
    url(r'^(?P<center_pk>[0-9]+)/(?P<urluniqueid>[0-9a-fA-F-]+)/data/$', DataView.as_view(), name='data_view'),
    url(r'^manager/$', ManagerIndex.as_view(), name='manager_index'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/$', ManagerDataView.as_view(), name='manager_data_view'),
    url(r'^manager/(?P<jobid>[0-9a-zA-Z-]+)/create_report/$', ManagerCreateReport.as_view(), name='create_report'),
]
