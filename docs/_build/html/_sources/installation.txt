Installation
********************

Apps
================
Install all of the apps mentioned in the README and/or requirements.txt.


App Changes
------------
If any of the apps use the User model (sorry I don't remember which), you need to replace it. Replace::

    from django.contrib.auth import User

with::

    from django.contrib.auth import get_user_model

And any instances of this::

    User

with this::

    get_user_model()


Django-registration change
+++++++++++++
In the directory of your external django apps (i.e. ``/usr/local/lib/python2.7``), go to ``registration/models.py`` and replace the ``create_inactive_user`` function with the below one::

    def create_inactive_user(self, username, email, password, user_type,
                                 site, send_email=True):
            """
            Create a new, inactive ``User``, generate a
            ``RegistrationProfile`` and email its activation key to the
            ``User``, returning the new ``User``.

            By default, an activation email will be sent to the new
            user. To disable this, pass ``send_email=False``.
        
            """
            new_user = get_user_model().objects.create_user(username, email, password, user_type=user_type)
            new_user.is_active = False
            new_user.save()

            registration_profile = self.create_profile(new_user)

            if send_email:
                registration_profile.send_activation_email(site)

            return new_user
        create_inactive_user = transaction.commit_on_success(create_inactive_user)

