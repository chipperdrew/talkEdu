.. YouTalkEdu documentation master file, created by
   sphinx-quickstart on Sun Aug 11 15:57:10 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to YouTalkEdu's documentation!
******************************************

Welcome! This is VERY much a work in progress, so hang tight!

YouTalkEdu was built on Django 1.6 using Python 2.7.


Apps
============
Outside of ``funct_tests``, there are 4 real apps, detailed below.


Posts
---------
If you can't find something, it's probably here.



Updating the docs
=====================
Navigate to ``talkEdu/docs/``, just simply run in the console::

    $ make_html


Testing
================
To run the tests, navigate to ``talkEdu/talkEdu/`` and run::

    $ python manage.py test

To run specific tests, i.e. the functional tests, run::

    $ python manage.py test funct_tests


Modifying the database
========================
If modifications are made to the database, simply run::

    $ python manage.py syncdb

If modifications are made to an app under the control of South (Accounts/posts/comments/votes), run::

    $ ./manage.py schemamigration APP_NAME --auto
    $ ./manage.py migrate APP_NAME



.. toctree::
   :maxdepth: 2



Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

