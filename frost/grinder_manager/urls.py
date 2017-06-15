from django.conf.urls import url

from .views import IndexView, GrinderJobSetup, create_job


app_name = 'grinder_manager'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^create/$', create_job, name='create_job'),
    url(r'^(?P<pk>[0-9]+)/setup/$', GrinderJobSetup.as_view(), name='job_setup'),
    # url(r'^(?P<job_id>[0-9]+)/add/$', add_field, name='add_field'),
    # url(r'^(?P<job_id>[0-9]+)/delete/$', delete_field, name='delete_field'),
    # url(r'^(?P<job_id>[0-9]+)/set/(?P<process_name>[0-9]+)/$', set_process_template, name='set_process_template'),
    # url(r'^(?P<job_id>[0-9]+)/set_job_name/$', set_job_name, name='set_job_name'),
    # url(r'^(?P<job_id>[0-9]+)/delete_job/$', delete_job, name='delete_job'),
]
