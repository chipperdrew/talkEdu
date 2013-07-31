from django.conf.urls import patterns, url

urlpatterns = patterns('comments.views',
    url(r'^new/(?P<post_id>\d+)/$', 'new_comment', name='new_comment'),
    url(r'delete/(?P<comment_id>\d+)/$', 'delete_comment', name='delete_comment'),
    url(r'^spam/(?P<id>\d+)/$', 'comment_mark_as_spam', name='comment_spam'),
    url(r'^show_replies/(?P<comment_id>\d+)/$', 'show_replies', name='show_replies'),

)
