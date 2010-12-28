from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djangosite/', include('djangosite.foo.urls')),
    (r'^purchase_order/$', 'nappy.views.po'),
    (r'^purchase_order/(?P<po_num>\d+)/$', 'nappy.views.singlepo'),
    (r'^stock/(?P<batch_num>\d+)/$', 'nappy.views.singlebatch'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
