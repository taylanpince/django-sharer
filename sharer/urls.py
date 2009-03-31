from django.conf.urls.defaults import *


urlpatterns = patterns('sharer.views',
    url(r'^$', 'share', name='sharer_share'),
    url(r'^done/$', 'share_done', name='sharer_done'),
)
