from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'posts.views.home_page', name='home'),
    url(r'^problems/$', 'posts.views.problems_page', name='problems'),
    url(r'^create_account/$','new_user_app.views.new_user_creation_page',
        name='createAccount'), #Name is reference in base.html

    url(r'^admin/', include(admin.site.urls)),
)
