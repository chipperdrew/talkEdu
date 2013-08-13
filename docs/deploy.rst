For deployment
*******************

Follow direction here: http://www.deploydjango.com/heroku/index.html

To see heroku accounts, type::
    
    $ heroku accounts


If you ever forget any info about your site, run::

    $ heroku info


To destroy, run::

    $ heroku apps:destroy youtalkedu


To create a Heroku application, run::

    $ heroku create --stack cedar deploydjango

To deploy::

    git push heroku master


The site is available at::

    http://youtalkedu.herokuapp.com/


To add a (free) database, type::

    $ heroku addons:add heroku-postgresql:dev
    $ heroku pg:info


Use the Django shell on the deployed app::

    $ heroku run python manage.py shell


DYNOS::

    $ heroku ps:scale web=1
    $ heroku ps


Config environ vars

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
