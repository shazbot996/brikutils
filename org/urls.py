from django.conf.urls import url

from . import views
from .views import MyOrgList, org_add, MyAssessList, assess_add, OrgUpdate, org_view, OrgDelete, AssessDelete, assess_view, AssessUpdate


urlpatterns = [
    url(r'^$', views.index, name='org_index'),
    url(r'^list$', MyOrgList.as_view(), name='org_list'),
    url(r'^add$', org_add, name="org_add"),
    url(r'^edit/(?P<pk>\d+)/$', OrgUpdate.as_view(), name='org_update'),
    url(r'^delete/(?P<pk>\d+)/$', OrgDelete.as_view(), name='org_delete'),
    url(r'^view/(\d+)/$', org_view, name='org_view'),
    url(r'^assessment$', MyAssessList.as_view(), name='assess_list'),
    url(r'^assessment/view/(\d+)/$', assess_view, name='assess_view'),
    url(r'^assessment/add$', assess_add, name="assess_add"),
    url(r'^assessment/edit/(?P<pk>\d+)/$', AssessUpdate.as_view(), name='assess_update'),

    url(r'^assessment/delete/(?P<pk>\d+)/$', AssessDelete.as_view(), name="assess_delete"),
]
