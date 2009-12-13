from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    #(r'^$', 'index'),
    #(r'^login/(?P<username>\w+)/(?P<password>\w+)/$', include('graffity.sketch.views.login')),
    (r'^login/$', 'graffity.sketch.views.login'),
    (r'^put/(?P<deviceid>\w+)/$', 'graffity.sketch.views.put'),
    (r'^get/(?P<deviceid>\w+)/$', 'graffity.sketch.views.get'),
    (r'^map/$', 'graffity.sketch.views.map'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': settings.STATIC_DOC_ROOT}),
)
