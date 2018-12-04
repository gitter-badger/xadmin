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
from material.frontend import urls as frontend_urls
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.contrib import admin

urlpatterns = [
    path(r'', xadmin.site.urls),
    # url(r'^$', generic.RedirectView.as_view(url='/workflow/', permanent=False)),
    # url(r'', include(frontend_urls)),
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
