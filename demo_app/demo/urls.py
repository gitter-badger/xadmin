# -*- coding: utf-8 -*-
# from django.conf.urls import include, url
from django.urls import include, path
import os
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.contrib import admin

urlpatterns = [
    path(r'', xadmin.site.urls),
]

# urlpatterns += [
#     path('<path:url>', views.flatpage),
# ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
