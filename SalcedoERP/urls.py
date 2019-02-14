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

import reporting
from Assistance import urls
import Assistance
from users import urls
import users
from ERP import urls
import ERP
from HumanResources import urls
import HumanResources
import Accounting
from Accounting import urls

from reporting import urls

from users import views

admin.autodiscover()

import DataUpload
from DataUpload import urls
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(users.urls)),
    url(r'^erp/', include(ERP.urls)),
    url(r'^accounting/', include(Accounting.urls)),
    url(r'^humanresources/', include(HumanResources.urls)),
    url(r'^assistance/', include(Assistance.urls)),
    url(r'^reporting/', include(ERP.urls)),
    url(r'^$', RedirectView.as_view(url='/admin')),
    url(r'^data_upload/', include(DataUpload.urls)),
    url(r'^reporting/', include(reporting.urls)),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^admin/empresas', users.views.empresas, name='empresas'),
    url(r'^admin/contratos', users.views.contratos, name='contratos'),

    url(r'^tinymce/', include('tinymce.urls')),

    #url(r'^inplaceeditform/', include('inplaceeditform.urls')),

    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
