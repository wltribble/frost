from django.conf.urls import url

from .views import IndexView, DetailView, PickTemplateView, save_data, edit_data, add_field, delete_field, set_process_template # set_job_name, submit, delete_job

app_name = 'polls'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/$', PickTemplateView.as_view(), name='pick_template'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/save/$', save_data, name='save_data'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/edit/$', edit_data, name='edit_data'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/add/$', add_field, name='add_field'),
    url(r'^(?P<urluniqueid>[0-9a-f-]+)/delete/$', delete_field, name='delete_field'),
    url(r'^(?P<jmouniqueid>[0-9a-f-]+)/set/(?P<process_name>[0-9]+)/$', set_process_template, name='set_process_template'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/set_job_name/$', set_job_name, name='set_job_name'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/submit/$', submit, name='submit'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/delete_job/$', delete_job, name='delete_job'),
]
