from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^events/(?P<topic>[^/]+)/$', views.events),
]
