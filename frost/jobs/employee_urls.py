from django.conf.urls import url

from .views import EmployeeIndexView

app_name = 'jobs'
urlpatterns = [
    url(r'^(?P<employee_id>[0-9a-zA-Z-]+)/$', EmployeeIndexView.as_view(), name='employee_index'),
]
