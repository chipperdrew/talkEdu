from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'posts.views.home_page', name='home'),

    url(r'^admin/', include(admin.site.urls)),
)
