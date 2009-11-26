from django.conf.urls.defaults import *

urlpatterns = patterns('graffity.sketch.views',
    #(r'^$', 'index'),
    #(r'^login/(?P<username>\w+)/(?P<password>\w+)/$', 'login'),
    (r'^login/$', 'login'),
    (r'^put/(?P<deviceid>\w+)/$', 'put'),
    (r'^get/(?P<deviceid>\w+)/$', 'get'),
)
