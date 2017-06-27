from django.conf.urls import url

from .views import IndexView, DetailView, PickTemplateView, save_data, edit_data, add_field, delete_field, set_process_template # submit

app_name = 'polls'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/$', PickTemplateView.as_view(), name='pick_template'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/save/$', save_data, name='save_data'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/edit/$', edit_data, name='edit_data'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/add/$', add_field, name='add_field'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/delete/$', delete_field, name='delete_field'),
    url(r'^(?P<urluniqueid>[0-9a-fA-F-]+)/set/(?P<process_name>[0-9]+)/$', set_process_template, name='set_process_template'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/set_job_name/$', set_job_name, name='set_job_name'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/submit/$', submit, name='submit'),
    # url(r'^(?P<jmouniqueid>[0-9]+)/delete_job/$', delete_job, name='delete_job'),
]
