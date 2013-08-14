For deployment
*******************

Follow direction here: http://www.deploydjango.com/heroku/index.html
Or better here: https://devcenter.heroku.com/articles/django

Set the following Heroku config vars:
- DJANGO_SETTINGS_MODULE
- All other env vars
- Make sure DATABASE_URL is set by heroku pg

After initial push, do the following:
 - heroku run python manage.py syncdb
 - heroku run python manage.py migrate accounts/posts/comments/votes

To collect staticfiles, run
$ python manage.py collectstatic



To see heroku accounts, type::
    
    $ heroku accounts


If you ever forget any info about your site, run::

    $ heroku info


To create a Heroku application, run::

    $ heroku create --stack cedar SITE_NAME


To destroy, run::

    $ heroku apps:destroy SITE_NAME


To deploy::

    $ git push heroku master
    $ heroku open


To add a (free) database and promote it (so DATABASE_URL is set), type::

    $ heroku addons:add heroku-postgresql:dev
    $ heroku pg:promote DB_NAME


This should create a free db and a URL link (which should be added to the heroku config). To check db::

    $ heroku pg:info


Use Django commands on the deployed app::

    $ heroku run python manage.py shell
    $ heroku run python manage.py syncdb
    $ heroku run python manage.py test
    $ heroku run python manage.py createsuperuser


DYNOS::

    $ heroku ps:scale web=1
    $ heroku ps


Config environ vars, or pull them from environment

    $ heroku config:pull --overwrite --interactive (NEED A CERTAIN APP FOR THIS, CAN'T REMEMBER WHAT)
    $ heroku config:set GITHUB_USERNAME=joesmith
    $ heroku config

Error checking::

    $ foreman start (to verify Procfile is set up correctly)
    $ heroku logs


According to Heroku
----------------

Set up virtualenv::

    $ pip install virtualenv
    $ virtualenv LOCATION --distribute

To enter and exit::

    $ source .venv/bin/activate
    $ deactivate
