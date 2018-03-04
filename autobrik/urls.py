from django.conf.urls import url

from . import views
from .views import new_vmdata, AllVMdataList


urlpatterns = [
    url(r'^$', views.index, name='autobrik_home'),
    url('upload/csv/$', views.upload_csv, name='upload_csv'),
    url(r'new_vmdata$', new_vmdata, name="autobrik_new_vmdata"),
    url(r'all$', AllVMdataList.as_view())
]
