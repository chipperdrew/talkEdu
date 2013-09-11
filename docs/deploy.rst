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


Heroku applications -- check, create, destroy::

    $ heroku apps
    $ heroku create --stack cedar SITE_NAME
    $ heroku apps:destroy SITE_NAME


To deploy::

    $ git push heroku master
    $ heroku open


Use Django commands on the deployed app::

    $ heroku run python manage.py shell
    $ heroku run python manage.py syncdb
    $ heroku run python manage.py test
    $ heroku run python manage.py createsuperuser


Error checking::

    $ foreman start (to verify Procfile is set up correctly)
    $ heroku logs


To set in maintenance mode, run::

    $ heroku maintenance:on/off
    $ heroku maintenance


Check the current release, and rollback if necessary

    $ heroku releases
    $ heroku releases:rollback vNUMBER

To add add-ons,
  
    $ heroku addons:add NAME:VERSION


Dynos, Databases, and Environment Variables
----------
Check dyno status and scale up/down::

    $ heroku ps:scale web=1
    $ heroku ps


To add a (free) database and promote it (so DATABASE_URL is set), type::

    $ heroku addons:add heroku-postgresql:dev
    $ heroku pg:promote DB_NAME
    $ heroku pg:info

Heroku pg-extra features (see https://github.com/heroku/heroku-pg-extras)::

   $ heroku plugins:install git://github.com/heroku/heroku-pg-extras.git
   $ heroku pg:cache_hit
   $ heroku pg:index_usage


Config environ vars, or pull them from environment::

    $ heroku config:pull --overwrite --interactive (NEED A CERTAIN APP FOR THIS, CAN'T REMEMBER WHAT)
    $ heroku config:set GITHUB_USERNAME=joesmith
    $ heroku config


Zerigo DNS
----------

    $ heroku addons:add zerigo_dns:basic
    $ heroku domains:add mydomain.com
    $ heroku domains:remove mydomain.com


PairNic name servers

     NS5.PAIRNIC.COM
     NS6.PAIRNIC.COM

Zerigo name servers (add NS Record from www >> )::
    
    A.NS.ZERIGO.NET
    ...
    E.NS.ZERIGO.NET

MX Records (for mail)::
  
    @ » 1 ASPMX.L.GOOGLE.COM.
    @ » 5 ALT2.ASPMX.L.GOOGLE.COM.
    @ » 5 ALT1.ASPMX.L.GOOGLE.COM.
    @ » 10 ASPMX3.GOOGLEMAIL.COM.
    @ » 10 ASPMX2.GOOGLEMAIL.COM. 

CNAME::

   @ >> youtalkedu.herokuapp.com (no SSL Endpoint)
   @ >> ENDPOINT_NAME.herokussl.com  (if SSL Endpoint)


Sentry -- Capture errors
-----------

    $ heroku addons:open sentry


Loggly -- Logging
-----------

    $ heroku addons:open loggly    

New relic -- Monitoring speeds, stats, etc.
----------

If deleted,
 - Edit Procfile
 - Removed LOGGING in settings
 - pip uninstall newrelic

Caching
--------------------
Steps when adding::

    $ heroku addons:add memcachier:dev

A bunch of CACHING stuff in settings, then::

    $ brew install libmemcached



Postgres backups
----------------
To create or delete a backup

    $ heroku pgbackups:capture
    $ heroku pgbackups:destroy BACKUP_ID
    $ heroku pgbackups

To create public backup url (use for migrations, upgrading plans, exporting data)::
    
    $ heroku pgbackups:url

If you need to restore DB (don't use unless you need it!!!!)::

    $ heroku pgbackups:restore DB_NAME BACKUP_ID (backup_id is optional, defaults to most recent)
    $ heroku pgbackups:restore HEROKU_POSTGRESQL_BLACK b251 


Endpoint SSL
------------
Install and add cert:

    $ heroku addons:add ssl:endpoint
    $ heroku certs:add Class1cert.crt ssl.key (may need --bypass)

If the key is password protected, type

    $ openssl rsa -in ssl.key -out newssl.unencrpyted.key

and use this cert. Now, adjust the CNAME DNS record.
