# -*- coding: utf-8 -*-
# from django.conf.urls import include, url
from django.urls import include, path
import os
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
import xadmin
from django.views import generic
from app.views import printLogin,printLogin1,printLogin2
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

# from material.frontend import urls as frontend_urls
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.contrib import admin

urlpatterns = [
    path(r'', xadmin.site.urls),
    # url(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),
    url(r'^printlogin/$', printLogin),
    url(r'^printlogin1/(\d+)$', printLogin1),
    url(r'^printlogin2/(\d+)$', printLogin2),
]

urlpatterns += [
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    re_path(r'^media/(?P<path>.*)$', login_required(serve), kwargs={'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# urlpatterns += [
#     path('<path:url>', views.flatpage),
# ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
