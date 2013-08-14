from django.conf.urls import patterns, include, url
from registrationFix.forms import MinPassLengthRegistrationForm
from registrationFix.views import CustomRegistrationView


urlpatterns = patterns('registrationFix.views',

    # Django-registration package
    url(r'^register/$', CustomRegistrationView.as_view(
        form_class=MinPassLengthRegistrationForm), name="register"),
    url(r'^', include('registration.backends.default.urls'),
        name='accounts'),
) 
