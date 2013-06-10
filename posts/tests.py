from django.test import Client, TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from posts.views import home_page, problems_page
from posts.models import Post


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        #expect_html = render_to_string('home.html')
        #self.assertEqual(response.content, expect_html)
        self.assertTemplateUsed(response, 'home.html')

    def test_not_logged_in_upon_arriving_to_home_page(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('Username:', response.content)
        self.assertIn('Password:', response.content)

class ProblemPageTest(TestCase):
    
    def test_prob_page_properly_opens_when_URL_accessed(self):
        client = Client()
        response = client.get('/problems/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'problems.html')

    def test_prob_page_can_save_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['post_content'] = 'A new post!'

        response = problems_page(request)

        # Checking database
        self.assertEqual(Post.objects.all().count(), 1)
        post1 = Post.objects.all()[0]
        self.assertEqual(post1.text, 'A new post!')

        self.assertEqual(response.status_code, 200)

    def test_prob_page_displays_posts(self):
        Post.objects.create(text='Post 1')
        Post.objects.create(text='Post 2')

        request = HttpRequest()
        response = problems_page(request)

        self.assertIn('Post 1', response.content)
        self.assertIn('Post 2', response.content)
        self.assertTemplateUsed(response, 'problems.html')
        

class PostModelTest(TestCase):

    def test_save_and_retrieve_posts(self):
        post1 = Post.objects.create(text = 'Post numero uno!')
        post2 = Post.objects.create(text = 'I love lamp?')

        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 2)

        saved_post1 = saved_posts[0]
        saved_post2 = saved_posts[1]
        self.assertEqual(saved_post1.text, 'Post numero uno!')
        self.assertEqual(saved_post2.text, 'I love lamp?')
