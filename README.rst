TODO:
=============
#) Fix sharing tags -- no image appearing for Facebook or Google+? 
#) Twitter- Have complaints about school or ideas for improvement? Let the world know by joining the discussion on YouTalkEdu.com
#) ASK PEOPLE TO USE AND TEST -- youtalkedu.herokuapp.com
#) Perform SSL identity check
#) AFTER TESTING - Change email registration links back
#) AFTER TESTING - Remove "on-click" and st_url attributes for social media links on home. do_not_hash=True
#) AFTER TESTING - Remove "testing" sign on home page
#) TIME PERMITTING - Option to change email?
#) TIME PERMITTING - Inherit models from django-registration so no need for entire registration app --- WILL TAKE TIME
#) TIME PERMITTING - Upgrade Bootstrap? --- WILL TAKE TIME b/c not backwards compat
#) TIME PERMITTING - Create a more personalized user page?
#) TIME PERMITTING - Allow for social auth using django-allauth
#) IN PRODUCTION - Log/count the spam caught by AKISMET, djangospam, honeypot
#) IN PRODUCTION - Make sure Django-axes is IP specific				---------------DO THIS NOW----------------
#) IN PRODUCTION - If reset db -- Change "Sites" in django admin
#) IF COMPLAINTS -  Have option to sort top-level comments by rating? -- CANNOT WORK WITH SHOW REPlIES. It won't know how to display (unless multiple for loops used)
#) IF COMPLAINTS - Save Akismet posts/comments that are being deemed spam
#) IF COMPLAINTS - Don't auto-delete "mark-as-spam" comments
#) IF COMPLAINTS - Smaller comment voting chart
#) IF COMPLAINTS - Load total comment count via AJAX also, thus accurate after comment deletion
#) IF COMPLAINTS - Make "sort-by" button and post delete AJAXed -- move "pages" logic into AJAX?
#) IF POPULAR - Change the "show_replies" link to prevent from reloading all comments --- create new template and append to comment_display as child of post?
#) IF POPULAR - Add more caching
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
#) FIXED - New posts will display on last page opened, not current page (bad session request)
#) DONE - 20 posts/page?
#) DONE - Create voting system
#) DONE - Add eduuser model to Accounts app, create Votes app
#) DONE - Implement "search" feature
#) DONE - Think of way to prevent post spam (created post limit and pot o' honey)
#) DONE - Add dropdown to sort posts by various categories (need voting system)
#) DONE - Implement option to mark a post as spam
#) DONE - Draw voting system
#) FIXED - By default, user login is cAsE sEnSiTiVe (however user creation is not)
#) DONE - Add FAQ page
#) DONE - Limit number of login attempts
#) DONE - Require certain password length/chars???
#) DONE - Fix error display on create account page
#) FIXED - Blank title posts work
#) DONE - Tell what the posts are sorted by
#) DONE - Dotted line through the center of votes for overall vote
#) DONE - Style post_page, add vote chart, up, down, etc
#) DON'T WANT 3 INSTANCE DICT IN CLASS - In post models, consider making up_votes and total_votes a dict, sorted by user_type? Then remove view logic
#) DONE - Allow for comments on POST pages (using Disqus? NO DISQUS IS EVIL)
#) DONE - Hide nested comments. Display if id in array path and length=??.
#) DONE - Add comment voting logic
#) DONE - Refactor logic to prevent excess filtering of votes by user type
#) NO - Save canvas chart and redraw when needed --- Canvas is actually pretty efficient (~2ms per post)
#) DONE - Update votes, spam marking on-the-fly with AJAX
#) DONE - Add AJAX to "show replies" on comments
#) NO - Add sort-by button to comments --- Pain to sort top-level comments and show replies in correct location
#) DONE - Add a Learn More page
#) DONE - Do something to prevent comment spam
#) DONE - Set up email with SMTP server
#) DONE - Pushed to the internet!!! 8/14/13
#) DONE - Add favicon (see w3 page)
#) DONE - Have comments load (via AJAX) AFTER post_page loads, display a loading screen.
#) DONE - Make "show" button in comments AJAXed
#) DONE - Fix reply chart from displaying after every reply click
#) DONE - TEDDY - Add logo/picture at top of tab
#) DONE - Compressed png images using http://tinypng.org/
#) DONE - Look into CACHING - https://docs.djangoproject.com/en/dev/topics/cache/


Basic Information
--------------------

* Site name: YouTalkEdu
* Created by: Andrew Cook


Installation Instructions
-----------------------------
* See the docs/ directory for installation instructions, specifically installation.rst


Thanks to the following
----------------------------
* General Learning:
	* Codecademy - http://www.codecademy.com/
	* Homebrew, Git, RVM, RoR Tutorial - http://www.moncefbelyamani.com/how-to-install-xcode-homebrew-git-rvm-ruby-on-mac/
	* Infographic on PHP vs Python vs Ruby - https://www.udemy.com/blog/modern-language-wars/
	* StackOverflow - http://stackoverflow.com/
	* StackOverflow (deserves to be mentioned again) - http://stackoverflow.com/

* General Services:
	* Python/IDLE - http://www.python.org/
	* Django - https://www.djangoproject.com/
	* Git - http://git-scm.com/
	* Github - https://github.com/
	* Twitter Bootstrap - http://twitter.github.io/bootstrap/index.html
	* Bootswatch - http://bootswatch.com/
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
	* Threaded Comments - http://maxburstein.com/blog/django-threaded-comments/

* Packages Used (Django related and others):
	* Boto (for AWS S3)
	* Coverage (for testing) - http://coverage.readthedocs.org/en/latest/
	* Django-axes (limit login attempts) - https://pypi.python.org/pypi/django-axes/1.3.3
	* Django-debug-toolbar (for debugging/site optimatization) - https://github.com/django-debug-toolbar/django-debug-toolbar
	* Django-storages (for AWS S3)
	* Django-haystack (for search functionality) - http://haystacksearch.org/
	* Django-model-utils (to use Choices) - https://pypi.python.org/pypi/django-model-utils
	* Django-picklefield (for dictionary model fields) - https://pypi.python.org/pypi/django-picklefield/
	* Django-registration (for creating/verifying user accounts) - http://django-registration.readthedocs.org/en/v1.0/index.html
	* Django-secure (for security, HTTPS, etc) - https://github.com/carljm/django-secure
	* Djangospam (for catching spam) - https://github.com/leandroarndt/djangospam
	* Pyelasticsearch (adapter to use ElasticSearch) - http://pyelasticsearch.readthedocs.org/en/latest/
	* Psycopg2 (needed to use PostgreSQL) - http://initd.org/psycopg/
	* Raven (for exception and to use Sentry)
	* Requests (Pyelasticsearch dependency) - https://django-request.readthedocs.org/en/latest/
	* Selenium (for testing) - http://docs.seleniumhq.org/
	* Simplejson (Pyelasticsearch dependency) - http://simplejson.readthedocs.org/en/latest/
	* South (for database migrations) - http://south.readthedocs.org/en/latest/index.html
	* Sphinx (installs Jinja2, MarkupSafe, Pygments, docutils) (for creating documention) - http://sphinx-doc.org/
