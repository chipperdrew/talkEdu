from django.conf.urls import patterns, url


urlpatterns = patterns('posts.views',
    url(r'^(?P<post_id>\d+)/$', 'post_page', name='post_page'), 

    # Create, edit, delete posts --- notice that create/edit call the same view
    url(r'^new/$', 'edit', name='post_new'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='post_edit'),
    url(r'^delete/(?P<id>\d+)/$', 'delete', name='post_delete'),
)
