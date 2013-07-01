from django.conf.urls import patterns, include, url
from django.contrib import admin

from registration.backends.default.views import RegistrationView
from posts.forms import CustomRegistrationForm

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
                       
    # Called if error on login. MAY WANT TO CHANGE TEMPLATE???
    url(r'^accounts/login/$', 'posts.views.login',
        {'template_name': 'base.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    # Django-registration package
    url(r'^accounts/register/$', RegistrationView.as_view(
        form_class=CustomRegistrationForm)),
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
