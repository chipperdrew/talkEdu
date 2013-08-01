from django.conf.urls import patterns, include, url
from accounts.forms import MinPassLengthRegistrationForm
from accounts.views import CustomRegistrationView


urlpatterns = patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout'),

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
        {'post_change_redirect': '/accounts/password/change/done/'},
        name='pass_change'),
    url(r'^password/change/done/$',
        'password_change_done'),
)


urlpatterns += patterns('accounts.views',
    url(r'^login/$', 'login',
        {'template_name': 'login.html'},
        name='login'),

    # Django-registration package
    url(r'^register/$', CustomRegistrationView.as_view(
        form_class=MinPassLengthRegistrationForm), name="register"),
    url(r'^', include('registration.backends.default.urls'),
        name='accounts'),

    # User type change
    url(r'^user_type/change/$', 'user_type_change',
        name='user_type_change'),
    url(r'^user_type/change/done/(?P<id>\d+)/$', 'user_type_change_done',
        name='user_type_change_done'),
)
