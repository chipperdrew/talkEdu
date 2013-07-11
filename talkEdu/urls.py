from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('posts.views',
    url(r'^$', 'home_page', name='home'),
    url(r'^problems/$', 'problems_page', name='problems'),
    url(r'^ideas/$', 'ideas_page', name='ideas'),
    url(r'^questions/$', 'questions_page', name='questions'),
    url(r'^site_feedback/$', 'site_feedback_page', name='site_feedback'),
    url(r'^user/(?P<user>[-\w]+)/$', 'user_page', name='user_page'),
)


urlpatterns += patterns('',
    url(r'^post/', include('posts.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^', include('votes.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
