from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from haystack.forms import SearchForm
from haystack.views import SearchView

admin.autodiscover()

urlpatterns = patterns('posts.views',
    url(r'^$', 'home_page', name='home'),
    url(r'faq/$', 'faq_page', name='faq'),
    url(r'learn/$', 'learn_more', name='learn_more'),
    url(r'^pages/(?P<page>[-\w]+)/$', 'display_page_helper', name='post_page_base'),
    url(r'^pages/(?P<page>[-\w]+)/(?P<sort_id>\d+)/$', 'display_page_helper', name='post_page_base'),
    url(r'^user/(?P<user>[-\w]+)/$', 'user_page', name='user_page'),
)


urlpatterns += patterns('',
    url(r'^' + settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^post/', include('posts.urls')),
    url(r'^comments/', include('djangospam.cookie.urls')), #IT'S A TRAP!
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('registrationFix.urls')),
    url(r'^', include('votes.urls')),
    url(r'^comment/', include('comments.urls')),
    url(r'^search/$', SearchView(form_class=SearchForm), name='search'),
)

# For deployment --- gathering up the static files
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if settings.DEBUG:
#urlpatterns += staticfiles_urlpatterns()
