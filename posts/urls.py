from django.conf.urls import patterns, url


urlpatterns = patterns('posts.views',
    url(r'^(?P<post_id>\d+)/$', 'post_page', name='post_page'),
    url(r'^(?P<post_id>\d+)/(?P<sort_id>\d+)/$', 'post_page', name='post_page'),
    url(r'^(?P<post_id>\d+)/all$', 'post_page', name='post_page_all'), #All comments

    # Create, edit, delete posts --- notice that create/edit call the same view
    url(r'^new/(?P<page_abbrev>[-\w]+)/$', 'edit', name='post_new'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='post_edit'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='post_delete'),
    url(r'^spam/(?P<id>\d+)/$', 'post_mark_as_spam', name='post_spam'),
)
