# Core Django imports
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import Client, TestCase
from django.utils import timezone

# App imports
from .views import home_page, problems_page
from .models import post, eduuser


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTemplateUsed(response, 'home.html')

    def test_not_logged_in_upon_arriving_to_home_page(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('Username:', response.content)
        self.assertIn('Password:', response.content)


class ProblemPageTest(TestCase):
    """
    Testing Problems page. Since other POST pages are similar,
    the some of the problems page tests are not duplicated elsewhere
    """
    
    def test_prob_page_properly_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/problems/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems.html')
    
    def test_prob_page_displays_only_its_posts(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass', user_type='PAR')
        post.objects.create(title='Post 1', user_id=new_user, page_type='PRO',
                            text='Additional text for Post 1')
        post.objects.create(title='Post 2', user_id=new_user, page_type='PRO')
        post.objects.create(title='Post 3', user_id=new_user, page_type='IDE')
        client = Client()
        response = client.get('/problems/')

        self.assertIn('Post 1', response.content)
        self.assertIn('Post 2', response.content)
        self.assertNotIn('Post 3', response.content)
        self.assertNotIn('Additional text', response.content)
        self.assertEqual(post.objects.all().filter(page_type='PRO').count(), 2)
        self.assertIn('Jim', response.content)
        self.assertIn('Parent', response.content)
        self.assertIn(str(timezone.now().day), response.content)
        self.assertTemplateUsed(response, 'problems.html')


class OtherPostPagesTest(TestCase):
    """
    Testing the other pages that accept POST requests besides Problems.
    This includes Ideas, Questions, and Site Feedback page
    """
    
    def test_ideas_page_properly_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/ideas/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas.html')
    
    def test_questions_page_properly_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/questions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions.html')

    def test_feedback_page_properly_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/site_feedback/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'site_feedback.html')

    def test_feedback_page_only_contains_its_posts(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        post.objects.create(title='Post 1', user_id=new_user, page_type='SIT')
        post.objects.create(title='Post 2', user_id=new_user, page_type='PRO')
        post.objects.create(title='Post 3', user_id=new_user, page_type='SIT')
        client = Client()
        response = client.get('/site_feedback/')

        self.assertIn('Post 1', response.content)
        self.assertIn('Post 3', response.content)
        self.assertNotIn('Post 2', response.content)
        self.assertEqual(post.objects.all().filter(page_type='SIT').count(), 2)


class AdditionalDisplayPagesTest(TestCase):
    
    def test_post_page_displays_title_and_text(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass', user_type='PAR')
        p1 = post.objects.create(title='Post 1', user_id=new_user,
                                 page_type='PRO', text='Additional text')
        client = Client()
        response = client.get('/post/' + str(p1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_page.html')
        self.assertIn('Post 1', response.content)
        self.assertIn('Additional text', response.content)

    def test_user_page_displays_username_and_posts(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass', user_type='PAR')
        post.objects.create(title='Post 1', user_id=new_user,
                                 page_type='PRO', text='Additional text')
        client = Client()
        response = client.get('/user/Jim/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_page.html')
        self.assertIn('Post 1', response.content)
        self.assertIn('Jim', response.content)

    
class PostModelTest(TestCase):
    
    def test_save_and_retrieve_posts(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        post1 = post.objects.create(title = 'Post numero uno!',
                                    user_id=new_user, text='Post 1 text')
        post2 = post.objects.create(title = 'I love lamp?', user_id=new_user)

        saved_posts = post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        saved_post1 = saved_posts[0]
        saved_post2 = saved_posts[1]
        self.assertEqual(saved_post1.title, 'Post numero uno!')
        self.assertEqual(saved_post1.text, 'Post 1 text')
        self.assertEqual(saved_post2.title, 'I love lamp?')

    def test_users_have_posts(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        new_user2 = eduuser.objects.create_user('Jane', 'chipperdrew@gmail.com',
                                            'pass')
        post1 = post.objects.create(title = 'Post numero uno!', user_id=new_user)
        post2 = post.objects.create(title = 'I love lamp?', user_id=new_user2)
        post3 = post.objects.create(title = '#3', user_id=new_user)

        all_users = eduuser.objects.all()
        self.assertEqual(all_users.count(), 2)
        user1 = all_users[0]
        user2 = all_users[1]
        self.assertEqual(user1.posts.count(), 2)
        self.assertEqual(user2.posts.count(), 1)
        self.assertEqual(user1.posts.all()[0].title, '#3')
        self.assertEqual(user2.posts.all()[0].title, 'I love lamp?')


# Consider moving tests below into separate user app
class UserRegistrationTest(TestCase):
    """
    Tests creation of user and access of URL page.
    Tests for interactions with registration form can be seen in funct_tests app
    """

    def test_save_and_retrieve_users(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        all_users = eduuser.objects.all()
        self.assertEqual(all_users.count(), 1)
        user1 = all_users[0]
        self.assertEqual(user1, new_user)
        self.assertEqual(user1.username, 'Jim')
        self.assertEqual(user1.email, 'chipperdrew@gmail.com')
    
    def test_register_page_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'registration/registration_form.html')


class UserLoginTest(TestCase):
    """
    Tests success of user login by examining redirects
    """
    
    def test_login_if_user_does_not_exist(self):
        client = Client()
        response = client.post('/accounts/login/',
                               {'usernane': 'Jim', 'password': 'pass'})
        self.assertEqual(response.status_code, 200) #No redirect => Failed
        
    def test_login_if_user_exists(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        client = Client()
        response = client.post('/accounts/login/',
                               {'username': 'Jim', 'password': 'pass'})
        self.assertEqual(response.status_code, 302) #Redirect => Passed

    def test_login_if_incorrect_pass(self):
        new_user = eduuser.objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        client = Client()
        response = client.post('/accounts/login/',
                               {'username': 'Jim', 'password': 'jim'})
        self.assertEqual(response.status_code, 200) #No redirect => Failed
        
        
        
