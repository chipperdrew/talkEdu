TODO:
=============
 
#) Read chapter on views
#) Use django-registration to create new users and verify login
#) Email users to confirm account
#) Allow users to enter in a name(title) in their posts
#) Display username and have delete option for posts (only for posts made by user)
#) DONE - Change database?
#) DONE - Create main template from which other templates inherit


Basic Information
--------------------

* Site name: YouTalkEdu
* Created by: Andrew Cook


Content Layout
-------------------
talkEdu/

	funct_tests/

		__init__.py

		tests_funct.py

	manage.py

	new_user_app/

		__init__.py

		tests_new_user.py

		views.py

	posts/

		__init__.py

		admin.py

		migrations/

		models.py

		tests_posts.py

		views.py

	README.rst

	requirements/
	
	static/

	talkEdu/

		__init__.py

		settings/

			__init__.py
			
			base.py

			local.py

			test.py

		urls.py

		wsgi.py

	templates/



Thanks to the following
----------------------------
* General Learning:
	* Codecademy - http://www.codecademy.com/
	* Homebrew, Git, RVM, RoR Tutorial - http://www.moncefbelyamani.com/how-to-install-xcode-homebrew-git-rvm-ruby-on-mac/
	* Infographic on PHP vs Python vs Ruby - https://www.udemy.com/blog/modern-language-wars/

* General Services:
	* Python/IDLE - http://www.python.org/
	* Django - https://www.djangoproject.com/
	* Git - http://git-scm.com/
	* Github - https://github.com/
	* Twitter Bootstrap - http://twitter.github.io/bootstrap/index.html
	* Selenium - http://docs.seleniumhq.org/
	* Homebrew - http://mxcl.github.io/homebrew/
	* MacVim - http://macvim.org/
	* PostgreSQL - http://www.postgresql.org/

* Django
	* Django installation Tutorial - http://osxwebdev.wordpress.com/2012/09/24/install-django-on-os-x-10-8-mountain-lion/
	* TDD Tutorial - http://chimera.labs.oreilly.com/books/1234000000754/index.html
	* The Django Book - http://www.djangobook.com/en/2.0/index.html
	* Django Documentation - https://docs.djangoproject.com/en/dev/
	* *Two Scoops of Django* - https://django.2scoops.org/

* Django Packages:
	* Coverage (for testing) - http://coverage.readthedocs.org/en/latest/#
	* Django-registration (for creating/verifying user accounts) - http://django-registration.readthedocs.org/en/v1.0/index.html
	* Psycopg2 (needed to use PostgreSQL) - http://initd.org/psycopg/
	* South (for database migrations) - http://south.readthedocs.org/en/latest/index.html

* Ruby on Rails
	* Rails for Zombies - http://railsforzombies.org/
