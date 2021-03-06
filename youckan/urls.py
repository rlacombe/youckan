# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

handler500 = 'youckan.views.server_error'

urlpatterns = patterns('',
    url('', include('youckan.apps.sso.urls')),
    url('', include('youckan.apps.accounts.urls')),
    # url('', include('youckan.data.urls')),
    url(r'^api/', include('youckan.api')),

    url(r'^js/', include('djangojs.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', include(admin.site.urls)),
)

# For debug
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'youckan.views.server_error'),
    )
