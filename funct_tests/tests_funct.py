# Stdlib imports

# Core Django imports
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase

# 3rd party imports
from selenium import webdriver, selenium
from selenium.webdriver.common.keys import Keys

# App imports
from posts.models import post

class NewVisitorTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        new_user = get_user_model().objects.create_user(
            'Test', 'chipperdrew@gmail.com', 'test',
            user_type=get_user_model().ADMINISTRATOR
        )
    def tearDown(self):
        self.browser.quit()

    def check_for_redirect_after_link_click(self, link_text,
                                            expected_url_regex):
        self.browser.find_element_by_link_text(link_text).click()
        self.browser.implicitly_wait(3)
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, expected_url_regex)

    def check_for_redirect_after_button_click(self, button_name,
                                              expected_url_regex):
        self.browser.find_element_by_name(button_name).click()
        self.browser.implicitly_wait(3)
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, expected_url_regex)

    def login_test_user(self):
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Test')
        pass_input.send_keys('test')
        self.browser.find_element_by_name('login').click()
      
    def test_home_page_has_proper_content_and_links(self):
        
        # Jim visits the home page of our site
        self.browser.get(self.live_server_url)

        # In the title are the words "Welcome To" and the word "Welcome" is
        # displayed on the page
        self.assertIn("Welcome to ", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome', header_text)

        # Jim is not logged in so the header contains login info
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn("Login", login_box)

        # Jim clicks on "Problems" link and is redirect to the problems page
        self.check_for_redirect_after_link_click("Problems", '/problems/$')
        
    def test_problems_page_posts_and_saves_content_when_logged_in(self):
        
        # The title of the problems page contains "Problems - "
        self.browser.get(self.live_server_url+'/problems/')
        self.assertIn("Problems - ", self.browser.title)

        # Jim logs in (as Test), and remains on the problems page
        self.login_test_user()
        self.assertIn("Problems - ", self.browser.title)
    
        # A title and text box are displayed
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Title:', page_text)
        self.assertIn('Text:', page_text)
        title_input = self.browser.find_element_by_name('title')
        
        # Jim types in "School is bad, mkay?"
        title_input.send_keys('School is bad, mkay?')

        # Jim presses enter. His post and username are displayed
        title_input.send_keys(Keys.ENTER)
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', page_text)
        self.assertIn('Test', page_text)

        # Jim types "I good at school". Jim clicks the "Post" button
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('I good at school')
        textbox_input = self.browser.find_element_by_name('text')
        textbox_input.send_keys('I really is')
        self.browser.find_element_by_id('id_post_button').click()

        # Both posts are displayed
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', page_text)
        self.assertIn('I good at school', page_text)
        self.assertIn('Posted by Test', page_text)
        self.assertNotIn('I really is', page_text)

        # Jim now clicks on his name and is redirected to the 'test' user page
        self.check_for_redirect_after_link_click('Test', '/user/Test/$')
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('I good at school', page_text)

        # Jim click on the 'Site Feedback', and does not see his posts
        self.check_for_redirect_after_link_click("Site Feedback",
                                                 '/site_feedback/$')
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('I good at school', page_text)
        self.assertNotIn('Posted by Test', page_text)

        # Jim now logs out
        self.check_for_redirect_after_button_click("logout",
                                                   self.live_server_url + '/$')

    def test_edit_and_deletion_of_posts(self):
        # Jim accesses the ideas page and logs in
        self.browser.get(self.live_server_url+'/ideas/')
        self.login_test_user()

        # Jim accidentally posts w/o entering text
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('Here is a')
        title_input.send_keys(Keys.ENTER)

        # Jim clicks the edit button and is properly redirected to edit page
        self.check_for_redirect_after_link_click('Edit', '/post/edit/')

        # Jim sees his post
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Title:', page_text)
        self.assertIn('Text:', page_text)

        # Jim changes his title and text
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys(' title')
        text_input = self.browser.find_element_by_name('text')
        text_input.send_keys('Here is some text')

        # Jim presses update and is returned to the ideas page
        self.check_for_redirect_after_button_click('update',
                                                   '/ideas/$')

        # Jim sees his updated title
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Here is a title', page_text)

        # Jim decides to delete his post
        self.browser.find_element_by_link_text("Delete").click()
        self.browser.switch_to_alert().accept()
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, '/ideas/$')

        # Jim no longer sees his post
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Here is a title', page_text)
           
    def test_problems_page_fails_to_post_when_not_logged_in(self):
        
        # Jim goes to the problems page and tries to post w/o logging in
        self.browser.get(self.live_server_url+'/problems/')
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('This should fail')
        self.assertIn('YouTalkEdu', self.browser.title)
        self.browser.find_element_by_id('id_post_button').click()
        self.assertNotIn('YouTalkEdu', self.browser.title) #error occurs
    
    def test_user_page_shows_proper_content_when_directly_accessed(self):

        # Jim accesses the 'Test' user page and sees the proper content
        self.browser.get(self.live_server_url+'/user/Test/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test', body)
        self.assertIn('Administrator', body)
        self.assertIn('User Test', self.browser.title)

    def test_change_password(self):
        # Jim logs in as test, as sees the link to his test's account page
        self.browser.get(self.live_server_url+'/ideas/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('My page', body)
        self.login_test_user()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('My page', body)

        # Jim clicks this link then clicks 'Change your password' link
        self.check_for_redirect_after_link_click('My page', '/user/Test/$')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Change your password', body)
        self.check_for_redirect_after_link_click('Change your password',
                                                 '/accounts/password/change/$')
        # Jim enters in his old password incorrectly
        old_pass = self.browser.find_element_by_id('id_old_password')
        new_pass1 = self.browser.find_element_by_id('id_new_password1')
        new_pass2 = self.browser.find_element_by_id('id_new_password2')
        old_pass.send_keys('BAD_PASS')
        new_pass1.send_keys('q')
        new_pass2.send_keys('q')
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/$')
        # Jim correctly fills out the form
        old_pass = self.browser.find_element_by_id('id_old_password')
        new_pass1 = self.browser.find_element_by_id('id_new_password1')
        new_pass2 = self.browser.find_element_by_id('id_new_password2')
        old_pass.send_keys('test')
        new_pass1.send_keys('q')
        new_pass2.send_keys('q')
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/done/$')
        # Jim logs out to test his new password
        self.check_for_redirect_after_button_click("logout",
                                                   self.live_server_url + '/$')

        # Jim tries to login with his old password and fails
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Test')
        pass_input.send_keys('test')
        self.check_for_redirect_after_button_click('login',
                                                   '/accounts/login/$')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Welcome Test', body)

        # Jim logs in with his new password
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Test')
        pass_input.send_keys('q')
        self.browser.find_element_by_name('login').click()
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome Test', body)

    def test_reset_password_link(self):
        # Jim goes to the site, clicks on reset password
        self.browser.get(self.live_server_url)
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Reset password', body)
        self.check_for_redirect_after_link_click('Reset password',
                                                 '/accounts/password/reset/$')
        # Jim sees the proper content, and enters in his email
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter your email', body)
        email = self.browser.find_element_by_id('id_email')
        email.send_keys('q@gmail.com')
        self.check_for_redirect_after_button_click('reset_pass_submit',
                                                   '/accounts/password/reset/done/$')
        ## Cannot access url emailed for resetting password...
     
    def test_user_creation_form(self):
        
        # On the homepage, Jim sees a place to create an account
        self.browser.get(self.live_server_url)
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Create Account', login_box)

        # Jim clicks the link and is redirected to a create account page
        self.check_for_redirect_after_link_click('Create Account',
                                                 '/accounts/register/$')

        # Jim sees 4 input boxes and a button
        inputs = self.browser.find_elements_by_tag_name('input')
        self.assertEqual(len(inputs), 11) # 5 header + 4 input + button + hidden
        
        # ATTEMPT 1: Jim (incorrectly) enters in his information
        # KEY: inputs 0-3 in header, 4 hidden in form, 5-8 inputs, 9 button
        inputs[6].send_keys('Jim')
        inputs[7].send_keys('chipperdrew@gmail.com')
        inputs[8].send_keys('Password')
        inputs[9].send_keys('Pazzword')
        self.browser.find_element_by_xpath("//select[@name='user_type']/option[text()='Teacher']").click()

        # Jim presses the "Create" button and is shown an error
        self.check_for_redirect_after_button_click(
            "create",
            self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The two password fields didn\'t match', body)

        # ATTEMPT 2: Jim (correctly) re-enters in his passwords
        # KEY: inputs 0-3 in header, 4 hidden in form, 5-8 inputs, 9 button
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[8].send_keys('Password')
        inputs[9].send_keys('Password')

        # Jim presses the "Create" button and sent to the complete page
        self.check_for_redirect_after_button_click(
            "create",
            self.live_server_url +'/accounts/register/complete/')

        ## 2 users are now created. Jim properties are saved
        ## Cannot access url emailed for confirming account...
        self.assertEqual(get_user_model().objects.all().count(), 2)
        jim = get_user_model().objects.all().get(username='Jim')
        self.assertEqual(jim.username, 'Jim')
        self.assertEqual(jim.email, 'chipperdrew@gmail.com')
        self.assertEqual(jim.get_user_type_display(), 'Teacher')

        # ATTEMPT 3: Jim (incorrectly) tries to create another 'Jim' account
        self.browser.get(self.live_server_url + '/accounts/register/')
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[6].send_keys('Jim')
        inputs[7].send_keys('chipperdrew@gmail.com')
        inputs[8].send_keys('P')
        inputs[9].send_keys('P')
        self.check_for_redirect_after_button_click(
            "create",
            self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('A user with that username already exists', body)

    def test_login_box_existance_and_redirect(self):
        
        # On the homepage, Jim sees a place to enter in his
        # username and password
        self.browser.get(self.live_server_url)
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Username:', login_box)
        self.assertIn('Password:', login_box)

        # Jim see enters his username and password into the appropriate boxes
        inputs = self.browser.find_elements_by_tag_name('input')
        self.assertEqual(len(inputs), 5) #hidden, user, pass, login, remember me
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Jim')
        pass_input.send_keys('Password')

        # Jim clicks the 'Login' button and is redirected to login page
        # b/c Jim's accounts DNE
        self.check_for_redirect_after_button_click('login', '/accounts/login/$')

        # Jim now decides to try to login on the Problems page
        self.browser.get(self.live_server_url+'/problems/')
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Username:', login_box)
        self.assertIn('Password:', login_box)

        # Jim (successfully) enters in his info,
        # clicks 'Login', and is redirected back to Problems page
        user = self.browser.find_element_by_id('id_user_login')
        password = self.browser.find_element_by_id('id_pass_login')
        user.send_keys('Test')
        password.send_keys('test')
        self.check_for_redirect_after_button_click('login', '/problems/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome Test', body)
    
    def test_pagination(self):
        # Jim visit a POST page and see 'Page 1 of 1'
        self.browser.get(self.live_server_url+'/questions/')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 1', body)
        test_user = get_user_model().objects.get(username='Test')
        for i in range(0,6): ## Modify this if change made to posts per page
            post.objects.create(title='Test post ' + str(i),
                            page_type=post.QUESTIONS,
                            user_id=test_user)

        # Multiple posts are created, some of which are pushed to a new page
        self.browser.get(self.live_server_url+'/questions/')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 2', body)
        self.assertIn('Next', body)

        # Jim goes to the next page
        self.check_for_redirect_after_link_click('Next', 'page=2$')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 2 of 2', body)
        self.assertIn('Previous', body)

        # Jim goes back to the previous page
        self.check_for_redirect_after_link_click('Previous', 'page=1$')
        body =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 2', body)
        self.assertIn('Next', body)


    # THIS TEST IS __NOT__ SAVING COOKIES. LOOK FOR NEW METHOD AND RE-RUN
    """
    def test_remember_me_feature(self):

        # Jim logs on as 'Test', w/o remember me
        self.browser.get(self.live_server_url)
        user = self.browser.find_element_by_id('id_user_login')
        password = self.browser.find_element_by_id('id_pass_login')
        user.send_keys('Test')
        password.send_keys('test')
        self.browser.find_element_by_name('login').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome Test', body)

        # Jim leaves and returns, but is no longer logged in
        self.browser.close()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Welcome Test', body)
        self.assertIn('Login', body)

        # Jim logs in again, but w/ remember me
        user = self.browser.find_element_by_id('id_user_login')
        password = self.browser.find_element_by_id('id_pass_login')
        user.send_keys('Test')
        password.send_keys('test')
        self.browser.find_element_by_name('remember_me').click()
        import time
        time.sleep(3)
        self.browser.find_element_by_name('login').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome Test', body)
        self.browser.implicitly_wait(3)

        # Jim leaves and returns, but is still logged in
        self.browser.close()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome Test', body)
        self.assertNotIn('Login', body)
     """

