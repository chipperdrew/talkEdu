TODO:
=============
#) Add eduuser model to accounts app?
#) Draw voting system
#) Allow for comments on POST pages (using django-comments)
#) Implement "search" feature
#) Implement option to mark a post as spam
#) Add dropdown to sort posts by various categories (need voting system)
#) Create a more personalized user page?
#) Think of way to prevent post spam
#) IN PRODUCTION - Set up email with SMTP server
#) IN PRODUCTION - Add https protection
#) TOFIX? - Require certain password length/chars???
#) TOFIX? - By default, user authorization is cAsE sEnSiTiVe (however user creation is not)
#) TOFIX? - Same as above, but with /user/chiPPeRdrew/ link
#) DONE - Change database?
#) DONE - Create main template from which other templates inherit
#) DONE - Use django-registration to create new users and verify login
#) DONE - Establish and display 'Post' to 'User' relationship (Many to one)
#) DONE - Create user profile (display name, # of posts)
#) DONE - Create remainder of pages, add database field so its knows what posts to show
#) DONE - Create "Remember me" feature
#) DONE - Allow users to enter in a name(title) in their posts
#) DONE - Create a field on registration form for stu/parent/teach/outsider/admin.
#) DONE - Have edit and delete option for posts made by logged-in user
#) DONE - Create change/reset password with django-registration
#) FIXED - New posts will display on last page opened, not current page (controlled by session request in views)
#) DONE - 20 posts/page?
#) DONE - Create voting system



Basic Information
--------------------

* Site name: YouTalkEdu
* Created by: Andrew Cook


Content Layout
-------------------
talkEdu/

	accounts/
		
		__init__.py

		forms.py

		models.py

		tests_accounts.py

		urls.py

		views.py
		

	funct_tests/

		__init__.py

		tests_funct.py

	htmlcov/

	manage.py

	posts/

		__init__.py

		admin.py

		forms.py

		migrations/

		models.py

		templatetags/

		tests_posts.py

		urls.py

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
	* StackOverflow - http://stackoverflow.com/

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
	* Resetting passwords - http://garmoncheg.blogspot.com/2012/07/django-resetting-passwords-with.html

* Django Packages:
	* Coverage (for testing) - http://coverage.readthedocs.org/en/latest/#
	* Django-registration (for creating/verifying user accounts) - http://django-registration.readthedocs.org/en/v1.0/index.html
	* Psycopg2 (needed to use PostgreSQL) - http://initd.org/psycopg/
	* South (for database migrations) - http://south.readthedocs.org/en/latest/index.html

* Ruby on Rails
	* Rails for Zombies - http://railsforzombies.org/
