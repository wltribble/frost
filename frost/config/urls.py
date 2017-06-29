from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<center_pk>[0-9]+)/jobs/', include('jobs.urls', namespace='jobs')),
    url(r'^', include('workcenters.urls', namespace='workcenters')),
]
