from django.conf.urls import url, include

from .views import IndexView, DetailView, PickTemplateView, save_data, edit_data, add_field, delete_field

app_name = 'polls'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', PickTemplateView.as_view(), name='pick_template'),
    url(r'^(?P<pk>[0-9]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<job_id>[0-9]+)/save/$', save_data, name='save_data'),
    url(r'^(?P<job_id>[0-9]+)/edit/$', edit_data, name='edit_data'),
    url(r'^(?P<job_id>[0-9]+)/add/$', add_field, name='add_field'),
    url(r'^(?P<job_id>[0-9]+)/delete/$', delete_field, name='delete_field'),
]
