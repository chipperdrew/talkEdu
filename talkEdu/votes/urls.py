from django.conf.urls import patterns, url

urlpatterns = patterns('votes.views',
    url(r'^up_vote/(?P<id>\d+)/(?P<item_type>[-\w]+)/$', 'up_vote', name='up_vote'),
    url(r'^down_vote/(?P<id>\d+)/(?P<item_type>[-\w]+)/$', 'down_vote', name='down_vote'),
)
