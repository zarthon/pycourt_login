from django.conf.urls.defaults import *
from pycourt_login.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pycourt_login/', include('pycourt_login.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$',index),
    (r'^login/',login),
    (r'^signup/',register),
    (r'^logout/',logout),
    (r'^forget/',forgot_password)
)

if settings.DEBUG:
    urlpatterns += patterns('',(r'^pycourt/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
        settings.MEDIA_ROOT}),)
