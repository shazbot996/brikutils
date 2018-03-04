from django.conf.urls import url

from . import views
from .views import viewrvt, upload, delrvt


urlpatterns = [
    url(r'^$', views.index, name='rvt_index'),
    url(r'^upload$', upload, name="rvt_upload"),
    url(r'^viewrvt$', viewrvt, name="rvt_view"),
    url(r'^viewrvt/(\d+)/$', viewrvt),
    url(r'^delete/(\d+)/$', delrvt, name='rvt_delete'),
]
