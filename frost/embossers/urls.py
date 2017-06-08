from django.conf.urls import url, include

from .views import IndexView, DetailView, save_data, edit_data, add_field

app_name = 'polls'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<job_id>[0-9]+)/save/$', save_data, name='save_data'),
    url(r'^(?P<job_id>[0-9]+)/edit/$', edit_data, name='edit_data'),
    url(r'^(?P<job_id>[0-9]+)/add/$', add_field, name='add_field'),
]
