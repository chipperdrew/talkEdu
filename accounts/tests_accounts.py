from django.test import Client, TestCase
from django.contrib.auth import get_user_model #Should be eduuser


class UserRegistrationTest(TestCase):
    """
    Test - User info is saved and retrievable, proper display on URL access
    """

    def test_save_and_retrieve_users(self):
        new_user = get_user_model().objects.create_user(
            'Jim', 'chipperdrew@gmail.com', 'pass'
        )
        all_users = get_user_model().objects.all()
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
    Test - Proper redirects when logging in
    """
    
    def test_login_if_user_does_not_exist(self):
        client = Client()
        response = client.post('/accounts/login/',
                               {'username': 'Jim', 'password': 'pass'})
        self.assertEqual(response.status_code, 200) #No redirect => Failed
        
    def test_login_if_user_exists(self):
        new_user = get_user_model().objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        client = Client()
        response = client.post('/accounts/login/',
                               {'username': 'Jim', 'password': 'pass'})
        self.assertEqual(response.status_code, 302) #Redirect => Passed

    def test_login_if_incorrect_pass(self):
        new_user = get_user_model().objects.create_user('Jim', 'chipperdrew@gmail.com',
                                            'pass')
        client = Client()
        response = client.post('/accounts/login/',
                               {'username': 'Jim', 'password': 'jim'})
        self.assertEqual(response.status_code, 200) #No redirect => Failed
        
        
        

