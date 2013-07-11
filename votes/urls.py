from django.conf.urls import patterns, url

urlpatterns = patterns('votes.views',
    url(r'^up_vote/(?P<id>\d+)/$', 'up_vote', name='up_vote'),
    url(r'^down_vote/(?P<id>\d+)/$', 'down_vote', name='down_vote'),
)
