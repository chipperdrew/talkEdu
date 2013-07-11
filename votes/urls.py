from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^up_vote/(?P<id>\d+)/$', 'votes.views.up_vote', name='up_vote'),
    url(r'^down_vote/(?P<id>\d+)/$', 'votes.views.down_vote', name='down_vote'),
)
