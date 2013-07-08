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

    # Create, edit, delete posts --- notice that create/edit call the same view
    url(r'^post/new/$', 'posts.views.edit', name='post_new'),
    url(r'^post/edit/(?P<id>\d+)/$', 'posts.views.edit', name='post_edit'),
    url(r'^post/delete/(?P<id>\d+)/$', 'posts.views.delete', name='post_delete'),
                       
    # Login/logout. Login called if init login error. CHANGE TEMPLATE???
    url(r'^accounts/login/$', 'posts.views.login',
        {'template_name': 'base.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),

    # Password reset
    url(r'^accounts/password/reset/$', #Initially called, sends email
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect': '/accounts/password/reset/done/'},
        name="password_reset"),
    url(r'^accounts/password/reset/done/$', #shows success message for email
        'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', #resets pass
        {'post_reset_redirect': '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', #shows success for resetting
        'django.contrib.auth.views.password_reset_complete'),

    # Password change
    url(r'^accounts/password/change/$',
        'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/accounts/password/change/done/'}),
    url(r'^accounts/password/change/done/$',
        'django.contrib.auth.views.password_change_done'),

    # Django-registration package
    url(r'^accounts/register/$', CustomRegistrationView.as_view(
        form_class=RegistrationForm)),
    url(r'^accounts/', include('registration.backends.default.urls'),
        name='accounts'),

    url(r'^admin/', include(admin.site.urls)),
)
