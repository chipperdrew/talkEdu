from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'posts.views.home_page', name='home'),
    url(r'^problems/$', 'posts.views.problems_page', name='problems'),
    url(r'^login/$', 'posts.views.login', name='login'),

# Django-registration package                      
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
