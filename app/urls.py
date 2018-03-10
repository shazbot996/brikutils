"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, me, initadmin

urlpatterns = [
    url(r'^$', index, name="app_index"),
    url(r'^me$',
        me,
        name="user_home"),
    url('login$',
        LoginView.as_view(template_name="app/app_login_form.html"),
        name="user_login"),
    url(r'logout$',
        LogoutView.as_view(),
        name="user_logout"),

    url(r'^admin/', admin.site.urls),
    url('^initadmin/', initadmin),

    url('^autobrik/', include('autobrik.urls')),
    url('^rvt/', include('rvt.urls')),
    url('^org/', include('org.urls')),
    url('^fusioncharts/', include('org.urls')),


    # EXAMPLE PARAMETER PASS
    # url(r'id_lookup/(?P<id>\d+)/$',
    #     id_lookup, name="module_id_lookup")
    #
    # THIS CAN BE REFERENCED IN HTML ALSO BY THIS:
    #
    # <a href="{% url 'module_id_lookup' id=module.id %}">

]
