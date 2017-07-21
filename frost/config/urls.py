from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^center/', include('jobs.urls', namespace='jobs')),
    url(r'^employee/', include('processes.urls', namespace='employees')),
    url(r'^', include('workcenters.urls', namespace='workcenters')),
]
