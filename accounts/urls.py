from django.conf.urls import patterns, include, url
from posts.forms import RegistrationForm    # Originally in django-registration
                                            # but updated in posts.forms
from posts.views import CustomRegistrationView


urlpatterns = patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout',
        {'next_page': '/'}),

    # Password reset
    url(r'^password/reset/$',
        'password_reset', 
        {'post_reset_redirect': '/accounts/password/reset/done/'},
        name="password_reset"),
    url(r'^password/reset/done/$',
        'password_reset_done'), 
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        {'post_reset_redirect': '/accounts/password/done/'}),
    url(r'^password/done/$',
        'password_reset_complete'),

    # Password change
    url(r'^password/change/$',
        'password_change',
        {'post_change_redirect': '/accounts/password/change/done/'}),
    url(r'^password/change/done/$',
        'password_change_done'),
)


urlpatterns += patterns('',
    # Login called if init login error. CHANGE TEMPLATE???
    url(r'^login/$', 'posts.views.login',
        {'template_name': 'base.html'}),

    # Django-registration package
    url(r'^register/$', CustomRegistrationView.as_view(
        form_class=RegistrationForm)),
    url(r'^', include('registration.backends.default.urls'),
        name='accounts'),
)
