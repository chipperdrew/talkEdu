from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'posts.views.home_page', name='home'),
    url(r'^problems/$', 'posts.views.problems_page', name='problems'),
    # Called if error on login. MAY WANT TO CHANGE TEMPLATE???
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'base.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'base.html'}),

    # Django-registration package                      
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
