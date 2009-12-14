from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^login/$', 'sketch.views.login'),
    (r'^put/(?P<deviceid>\w+)/$', 'sketch.views.put'),
    (r'^strokes/(?P<lat>[\w\.]+)/(?P<lon>[\w\.]+)$','sketch.views.strokes'),

    (r'^map/$', 'sketch.views.map'),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': settings.MEDIA_ROOT}),
)
