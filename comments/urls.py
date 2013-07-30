from django.conf.urls import patterns, url

urlpatterns = patterns('comments.views',
    url(r'^new/(?P<post_id>\d+)/$', 'new_comment', name='new_comment'),
    url(r'delete/(?P<comment_id>\d+)/$', 'delete_comment', name='delete_comment'),
)
