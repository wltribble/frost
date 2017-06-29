from django.conf.urls import url, include

from .views import PickCenterView


app_name = 'workcenters'
urlpatterns = [
    url(r'^', PickCenterView.as_view(), name='pick_center'),
]
