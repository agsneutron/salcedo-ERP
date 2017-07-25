"""SalcedoERP URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect
from django.conf import settings
from users import urls
import users
from ERP import urls
import ERP

from users import views
admin.autodiscover()

import DataUpload
from DataUpload import urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(users.urls)),
    url(r'^erp/', include(ERP.urls)),
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^data_upload/', include(DataUpload.urls)),
]
