from django.conf.urls import patterns, include, url
from django.contrib import admin
from posts.forms import RegistrationForm    # Originally in django-registration
                                            # but updated in posts.forms
from posts.views import CustomRegistrationView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'posts.views.home_page', name='home'),
    url(r'^problems/$', 'posts.views.problems_page', name='problems'),
    url(r'^ideas/$', 'posts.views.ideas_page', name='ideas'),
    url(r'^questions/$', 'posts.views.questions_page', name='questions'),
    url(r'^site_feedback/$', 'posts.views.site_feedback_page',
        name='site_feedback'),
    url(r'^user/(?P<user>[-\w]+)/$', 'posts.views.user_page',
        name='user_page'),
    url(r'^post/(?P<post_id>\d+)/$', 'posts.views.post_page',
        name='post_page'),

    url(r'^post/edit/(?P<id>\d+)/$', 'posts.views.edit', name='post_edit'),
    url(r'^post/new/$', 'posts.views.edit', name='post_new'),

                      
    # Called if error on login. MAY WANT TO CHANGE TEMPLATE???
    url(r'^accounts/login/$', 'posts.views.login',
        {'template_name': 'base.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    # Django-registration package
    url(r'^accounts/register/$', CustomRegistrationView.as_view(
        form_class=RegistrationForm)),
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
