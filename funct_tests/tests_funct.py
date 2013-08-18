# Stdlib imports
import time

# Core Django imports
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase

# 3rd party imports
from selenium import webdriver, selenium
from selenium.webdriver.common.keys import Keys

# App imports
from posts.models import post
from comments.models import comment
from votes.models import spam


class NewVisitorTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        get_user_model().objects.create_user(
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

    def login_user(self, username, password):
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys(username)
        pass_input.send_keys(password)
        self.browser.find_element_by_name('login').click()
    
    def test_home_page_has_proper_content_and_links(self):
        
        # Jim visits the home page of our site
        self.browser.get(self.live_server_url)

        # In the title are the words "Welcome To" and the word "Welcome" is
        # displayed on the page
        self.assertIn("Welcome to ", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('talk education', header_text)

        # Jim is not logged in so the header contains login info
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn("Login", body)

        # Jim clicks on "Problems" link and is redirect to the problems page
        self.check_for_redirect_after_link_click("Problems", '/problems/$')
    
    def test_learn_more_page_has_proper_content_and_links(self):
        
        # Jim visits the learn more page of our site
        self.browser.get(self.live_server_url+'/learn/')

        # The proper content is displayed
        self.assertIn('Learn', self.browser.title)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Welcome to', body)
        self.assertIn('PIQS pages', body)

        # Jim accesses the page via the "Learn" tab
        self.browser.find_element_by_link_text('YouTalkEdu').click()
        self.browser.find_element_by_link_text('Learn').click()
        self.assertEqual(self.browser.current_url, self.live_server_url+'/learn/')
        
    def test_posts_are_saved_and_properly_displayed(self):
        
        # Jim does not sees the text boxes on the 'Problems' page w/o login
        self.browser.get(self.live_server_url+'/pages/problems/')
        self.assertIn("Problems - ", self.browser.title)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Title:', body)
        self.assertNotIn('Text:', body)

        # Jim logs in (as Test), and is returned to the problems page
        self.check_for_redirect_after_link_click('Login', '/accounts/login/')
        self.login_user('Test', 'test')
        self.assertIn("Problems - YouTalkEdu", self.browser.title)

        # A link saying "Click me to create a post" is displayed. Jim clicks it
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Title:', body)
        self.assertNotIn('Text:', body)
        self.assertIn('Click me to create a post', body)
        self.browser.find_element_by_id('id_show_form').click()
    
        # A title and text box are now displayed
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Title:', body)
        self.assertIn('Text:', body)
        self.assertNotIn('Click me to create a post', body)
        title_input = self.browser.find_element_by_name('title')
        
        # Jim types in "School is bad, mkay?"
        title_input.send_keys('School is bad, mkay?')

        # Jim presses enter. His post and username are displayed
        title_input.send_keys(Keys.ENTER)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', body)
        self.assertIn('Test', body)

        # Jim click the link to post, types "I good at school", and
        # clicks the "Post" button
        self.browser.find_element_by_id('id_show_form').click()
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('I good at school')
        textbox_input = self.browser.find_element_by_name('text')
        textbox_input.send_keys('I really is')
        self.browser.find_element_by_name('post_button').click()

        # Both posts titles are displayed, but the text is not
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', body)
        self.assertIn('I good at school', body)
        self.assertIn('Test posted', body)
        self.assertNotIn('I really is', body)

        # Jim now clicks on his name and is redirected to the 'test' user page
        self.check_for_redirect_after_link_click('Test', '/user/Test/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('I good at school', body)

        # Jim click on the 'Site Feedback', and does not see his posts
        self.check_for_redirect_after_link_click("Site Feedback",
                                                 '/site_feedback/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('I good at school', body)
        self.assertNotIn('Test posted', body)

        # Jim tries to post w/o entering in a title
        self.browser.find_element_by_id('id_show_form').click()
        self.check_for_redirect_after_button_click('post_button',
                                                   '/site_feedback/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a title', body)
        self.assertNotIn('Click me to create a post', body)

        # Jim tries to post with a white-space only title
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('  ')
        self.check_for_redirect_after_button_click('post_button',
                                                   '/site_feedback/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a valid title', body)

        # Jim tries to test the posting limit
        self.browser.get(self.live_server_url+'/pages/problems/')
        for i in range(0,3):
            self.browser.find_element_by_id('id_show_form').click()
            title_input = self.browser.find_element_by_name('title')
            title_input.send_keys('Test Post')
            self.browser.find_element_by_name('post_button').click()

        # On his 6th attempt, he is told he cannot post anymore
        self.browser.find_element_by_id('id_show_form').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You have used up all of your posts', body)

        # Jim now logs out and is returns to the current page
        self.check_for_redirect_after_button_click("logout_nav",
                                                   self.live_server_url + '/pages/problems/$')
    
    def test_edit_and_deletion_of_posts(self):
        # Jim logs in then goes to the ideas page
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('Test', 'test')
        self.assertRegexpMatches(self.browser.current_url,
                                 self.live_server_url+'/$')
        self.browser.get(self.live_server_url+'/pages/ideas/')

        # Jim accidentally posts w/o entering text
        self.browser.find_element_by_id('id_show_form').click()
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('Here is a')
        title_input.send_keys(Keys.ENTER)

        # Jim clicks the edit button and is properly redirected to edit page
        self.check_for_redirect_after_link_click('Edit', '/post/edit/')

        # Jim sees his post
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Title:', body)
        self.assertIn('Text:', body)

        # Jim tries to create an error by removing his title, but sees an error
        title_input = self.browser.find_element_by_name('title')
        title_input.clear()
        self.check_for_redirect_after_button_click('update', '/edit/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a title', body)
        
        # Jim changes his title and text
        title_input = self.browser.find_element_by_name('title')
        title_input.send_keys('Here is a title')
        text_input = self.browser.find_element_by_name('text')
        text_input.send_keys('Here is some text')

        # Jim presses update and is returned to the ideas page
        self.check_for_redirect_after_button_click('update', '/ideas/')

        # Jim sees his updated title
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Here is a title', body)

        # Jim decides to delete his post
        self.browser.find_element_by_link_text("Delete").click()
        self.browser.switch_to_alert().accept()
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, '/ideas/')

        # Jim no longer sees his post
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Here is a title', body)
        
    def test_user_page_shows_proper_content_when_directly_accessed(self):
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(title='Title', user_id=test_user)

        # Jim accesses the 'Test' user page and sees the proper content
        self.browser.get(self.live_server_url+'/user/Test/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test', body)
        self.assertIn('Administrator', body)
        self.assertIn('Last logged in on', body)
        self.assertIn('1: ', body)
        self.assertIn('Title', body)
        self.assertIn('Overall Rating', body)
        self.assertIn('0.0', body)
        self.assertIn('(0 votes)', body)
        self.assertIn('User Test', self.browser.title)
        self.assertNotIn('Change your password', body)

        # Jim logsin and sees specific content for him
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Change your password', body)
        self.assertIn('chipperdrew@gmail.com', body)
        
    
    def test_post_page_shows_proper_content(self):
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(title='Test post', text='Some text',
                            page_type=post.QUESTIONS,
                            user_id=test_user)

        # Jim visits his posts page and sees the proper content
        self.browser.get(self.live_server_url+'/pages/questions/')
        self.browser.find_element_by_link_text('Test post').click()
        self.assertRegexpMatches(self.browser.current_url, 'post/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test post', body)
        self.assertIn('Some text', body)
        self.assertIn('Test', body)
        self.assertIn('Administrator', body)
        self.assertIn('Posted at', body)
        self.assertIn('Overall: 0.0', body)
        self.assertIn('Total Votes: 0', body)
        self.assertNotIn('Up', body)
        self.assertNotIn('Edit', body)

        # Jim logs in and sees some links
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Up', body)
        self.assertIn('Edit', body)

        # Jim votes and sees the effect
        self.browser.find_element_by_link_text('Up').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall: 1.0', body)
        self.assertIn('Total Votes: 1', body)

        # Jim changes his vote
        self.browser.find_element_by_link_text('Down').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall: 0.0', body)
        self.assertIn('Total Votes: 1', body)

        # Jim deletes his post and is redirected
        self.browser.find_element_by_link_text('Delete').click()
        self.browser.switch_to_alert().accept()
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, self.live_server_url+'/$')
    
    def test_change_password(self):
        # Jim logs in as test, as sees the link to his test's account page
        self.browser.get(self.live_server_url+'/accounts/login/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Test', body)
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test', body)

        # Jim clicks this link then clicks 'Change your password' link
        self.check_for_redirect_after_link_click('Test', '/user/Test/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Change your password', body)
        self.check_for_redirect_after_link_click('Change your password',
                                                 '/accounts/password/change/$')

        # Jim presses enter w/o filling out the form
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter your old password', body)
        self.assertIn('Please enter a new password', body)

        # 1: Jim enters too short of a password
        old_pass = self.browser.find_element_by_id('id_old_password')
        new_pass1 = self.browser.find_element_by_id('id_new_password1')
        new_pass2 = self.browser.find_element_by_id('id_new_password2')
        old_pass.send_keys('test')
        new_pass1.send_keys('q')
        new_pass2.send_keys('q')
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Password must have at least', body)


        # 2: Jim enters his old pass incorrect & 2 diff passwords
        old_pass = self.browser.find_element_by_id('id_old_password')
        new_pass1 = self.browser.find_element_by_id('id_new_password1')
        new_pass2 = self.browser.find_element_by_id('id_new_password2')
        old_pass.send_keys('BAD_PASS')
        new_pass1.send_keys('test1234')
        new_pass2.send_keys('test123456')
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('old password was entered incorrectly', body)
        self.assertIn('two password fields didn\'t match', body)
        
        # 3: Jim correctly fills out the form
        old_pass = self.browser.find_element_by_id('id_old_password')
        new_pass1 = self.browser.find_element_by_id('id_new_password1')
        new_pass2 = self.browser.find_element_by_id('id_new_password2')
        old_pass.send_keys('test')
        new_pass1.send_keys('test1234')
        new_pass2.send_keys('test1234')
        self.check_for_redirect_after_button_click('pass_change_submit',
                                                   '/accounts/password/change/done/$')
        # Jim logs out to test his new password
        self.check_for_redirect_after_button_click("logout_nav",
                                                   self.live_server_url + '/accounts/login/')

        # Jim tries to login with his old password and fails
        self.browser.get(self.live_server_url+'/accounts/login/')
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Test')
        pass_input.send_keys('test')
        self.check_for_redirect_after_button_click('login',
                                                   '/accounts/login/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Welcome Test', body)

        # Jim logs in with his new password
        user_input = self.browser.find_element_by_id('id_user_login')
        pass_input = self.browser.find_element_by_id('id_pass_login')
        user_input.send_keys('Test')
        pass_input.send_keys('test1234')
        self.browser.find_element_by_name('login').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Test', body)
    
    def test_reset_password_link(self):
        # Jim goes to the site, clicks on reset password
        self.browser.get(self.live_server_url+'/accounts/login/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Forgot my password', body)
        self.check_for_redirect_after_link_click('Forgot my password',
                                                 '/accounts/password/reset/$')

        # Jim sees the proper content and clicks the button w/o entering info
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter your email', body)
        self.check_for_redirect_after_button_click('reset_pass_submit',
                                                   '/accounts/password/reset/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('This field is required.', body)
        
        # Jim sees the proper content, and enters in an invalid email
        email = self.browser.find_element_by_id('id_email')
        email.send_keys('q@gmail.com')
        self.check_for_redirect_after_button_click('reset_pass_submit',
                                                   '/accounts/password/reset/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('email address is not registered', body)

        # Jim now enters in his proper email
        email = self.browser.find_element_by_id('id_email')
        email.clear()
        email.send_keys('chipperdrew@gmail.com')
        self.check_for_redirect_after_button_click('reset_pass_submit',
                                                   '/accounts/password/reset/done/$')
        ## Cannot access url emailed for resetting password...
    
    def test_user_creation_form(self):
        
        # On the login page, Jim sees a place to create an account
        self.browser.get(self.live_server_url+'/accounts/login/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Create an account', body)

        # Jim clicks the link and is redirected to a create account page
        self.check_for_redirect_after_link_click('Create an account',
                                                 '/accounts/register/$')

        # ATTEMPT 0: Jim clicks enter withot entering in anything
        self.check_for_redirect_after_button_click(
            "create", self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a username', body)
        self.assertIn('Please enter a valid email', body)
        self.assertIn('Please enter a password', body)
        self.assertIn('Please verify your password', body)


        # Jim sees 4 input boxes and a button
        inputs = self.browser.find_elements_by_tag_name('input')
        self.assertEqual(len(inputs), 5) # 4 input + hidden

        # ATTEMPT 0.5: Jim creates too short of a password:
        # KEY: 0 is hidden in form, 1-4 are inputs
        inputs[1].send_keys('Jim')
        inputs[2].send_keys('youtalkedu@gmail.com')
        inputs[3].send_keys('Pass')
        inputs[4].send_keys('Pass')
        self.check_for_redirect_after_button_click(
            "create", self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Password must have at least', body)
        
        # ATTEMPT 1: Jim enters in non-matching passwords
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[3].send_keys('Password')
        inputs[4].send_keys('Pazzword')
        self.browser.find_element_by_xpath("//select[@name='user_type']/option[text()='Teacher']").click()
        self.check_for_redirect_after_button_click(
            "create", self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('The two password fields didn\'t match', body)

        # ATTEMPT 2: Jim (correctly) re-enters in his passwords
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[3].send_keys('Password')
        inputs[4].send_keys('Password')
        self.check_for_redirect_after_button_click(
            "create",
            self.live_server_url +'/accounts/register/complete')

        ## 2 users are now created. Jim properties are saved
        ## Cannot access url emailed for confirming account...
        self.assertEqual(get_user_model().objects.all().count(), 2)
        jim = get_user_model().objects.all().get(username='Jim')
        self.assertEqual(jim.username, 'Jim')
        self.assertEqual(jim.email, 'youtalkedu@gmail.com')
        self.assertEqual(jim.get_user_type_display(), 'Teacher')

        # ATTEMPT 3: Jim (incorrectly) tries to create another 'Jim' account
        self.browser.get(self.live_server_url + '/accounts/register/')
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[1].send_keys('Jim')
        inputs[2].send_keys('youtalkedu@gmail.com')
        inputs[3].send_keys('P')
        inputs[4].send_keys('P')
        self.check_for_redirect_after_button_click(
            "create",
            self.live_server_url +'/accounts/register/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('A user with that username already exists', body)
        self.assertIn('This email address is already in use.', body)
    
    def test_pagination(self):
        # Jim visit a POST page and see 'Page 1 of 1'
        self.browser.get(self.live_server_url+'/pages/questions/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 1', body)
        test_user = get_user_model().objects.get(username='Test')
        for i in range(0,6): ## Modify this if change made to posts per page
            post.objects.create(title='Test post ' + str(i),
                            page_type=post.QUESTIONS,
                            user_id=test_user)

        # Multiple posts are created, some of which are pushed to a new page
        self.browser.get(self.live_server_url+'/pages/questions/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 2', body)
        self.assertIn('Next', body)

        # Jim goes to the next page
        self.check_for_redirect_after_link_click('Next', 'page=2$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 2 of 2', body)
        self.assertIn('Previous', body)

        # Jim goes back to the previous page
        self.check_for_redirect_after_link_click('Previous', 'page=1$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Page 1 of 2', body)
        self.assertIn('Next', body)
    
    def test_vote_existance_and_functionality(self):
        test_user = get_user_model().objects.get(username='Test')
        t1 = post.objects.create(title='T1', page_type=post.IDEAS, user_id=test_user)
        post.objects.create(title='T2', page_type=post.IDEAS, user_id=test_user)

        # Jim visits the ideas page, sees the voting info, but cannot vote
        self.browser.get(self.live_server_url+'/pages/ideas/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Up', body)
        self.assertNotIn('Down', body)

        # Jim logs in, sees the current votes, and can vote
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall: 0.0', body)
        self.assertIn('Up', body)
        self.assertIn('Down', body)
        up_votes = self.browser.find_elements_by_link_text('Up')
        self.assertEqual(len(up_votes), 2)

        # Jim clicks the 'up' vote for one of the posts
        up_votes[0].click()
        time.sleep(1)
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, self.live_server_url+'/pages/ideas/')

        # Jim sees his vote
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn("Overall: 1.0", body)
        self.assertIn("Total Votes: 1", body)

        # Jim tries to directly access the vote url & gets a 404. He logs out
        self.browser.get(self.live_server_url+'/up_vote/'+ str(t1.id) + '/p')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Not Found', body)
        self.browser.get(self.live_server_url+'/accounts/logout/')
        
        # Bob, another user, logs in and sees the posts
        get_user_model().objects.create_user(
            'Bob', 'chipperdrew@gmail.com', 'b',
            user_type=get_user_model().ADMINISTRATOR
        )
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('Bob', 'b')
        self.check_for_redirect_after_link_click('Ideas', '/ideas/$')

        # Bob votes on the same post
        down_votes = self.browser.find_elements_by_link_text('Down')
        down_votes[0].click()
        time.sleep(1)
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, self.live_server_url+'/pages/ideas/')

        # Bob sees how his vote has changed the voting value
        body = self.browser.find_element_by_tag_name('body').text
        self.browser.find_element_by_name('logout_nav').click()

        # Jill, a student, logs in
        get_user_model().objects.create_user(
            'Jill', 'chipperdrew@gmail.com', 'j',
            user_type=get_user_model().STUDENT
        )
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('Jill', 'j')
        self.check_for_redirect_after_link_click('Ideas', '/ideas/$')
        
        # Jill votes and sees the changes
        up_votes = self.browser.find_elements_by_link_text('Up')
        up_votes[0].click()
        time.sleep(1)
        new_url = self.browser.current_url
        self.assertRegexpMatches(new_url, self.live_server_url+'/pages/ideas/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall: 0.667', body)
        self.assertIn('Total Votes: 3', body)
        self.assertIn('Overall: 0.0', body)
        self.assertIn('Total Votes: 0', body)
    
    def test_comment_voting(self):
        test_user = get_user_model().objects.get(username='Test')
        p1 = post.objects.create(title='T1', page_type=post.IDEAS, user_id=test_user)

        # Jim creates a comment and sees the voting options
        self.browser.get(self.live_server_url+'/pages/ideas/')
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        self.browser.find_element_by_link_text('T1').click()
        self.browser.find_element_by_id('id_content').send_keys('Comment 1')
        self.browser.find_element_by_name('comment_button').click()
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Up', comment_display)
        self.assertIn('Overall: 0.0', comment_display)
        self.assertIn('Total Votes: 0', comment_display)

        # Jim logs out and does not see the option to vote
        self.browser.find_element_by_link_text('Logout').click()
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertNotIn('Up', comment_display)
        self.assertIn('Overall: 0.0', comment_display)
        self.assertIn('Total Votes: 0', comment_display)

        # Jim logs back in, votes "Up", & sees the proper content
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        up_votes = self.browser.find_elements_by_link_text('Up')
        up_votes[1].click() #[0] - post vote, [1] - comment vote
        time.sleep(1)
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Overall: 1.0', comment_display)
        self.assertIn('Total Votes: 1', comment_display)

        # Jim tries to vote again -- nothing changes
        up_votes = self.browser.find_elements_by_link_text('Up')
        up_votes[1].click()
        time.sleep(1)
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Overall: 1.0', comment_display)
        self.assertIn('Total Votes: 1', comment_display)

        # Jim votes down and the proper content changes
        down_votes = self.browser.find_elements_by_link_text('Down')
        down_votes[1].click()
        time.sleep(1)
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Overall: 0.0', comment_display)
        self.assertIn('Total Votes: 1', comment_display)
    
    def test_user_voting_numbers_are_stored_properly(self):
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(title='T1', page_type=post.PROBLEMS, user_id=test_user)
        post.objects.create(title='T2', page_type=post.IDEAS, user_id=test_user)
        post.objects.create(title='T3', page_type=post.QUESTIONS, user_id=test_user)

        # Jim logs in, visits the problems page, and votes up
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('Test', 'test')
        self.browser.get(self.live_server_url+'/pages/problems/')
        self.browser.find_element_by_link_text('Up').click()
        time.sleep(1)

        # Jim goes the the ideas page and votes down
        self.browser.get(self.live_server_url+'/pages/ideas/')
        self.browser.find_element_by_link_text('Down').click()
        time.sleep(1)

        # Jim goes the questions page and votes up
        self.browser.get(self.live_server_url+'/pages/questions/')
        self.browser.find_element_by_link_text('Up').click()
        time.sleep(1)

        # Jim goes to his user page and sees the proper vote percentage
        self.check_for_redirect_after_link_click('Test', '/user/Test/$')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall user rating: 0.667', body)

        # Jim changes his vote, goes to his user page, and sees the updated perc
        self.browser.get(self.live_server_url+'/pages/questions/')
        self.browser.find_element_by_link_text('Down').click()
        time.sleep(1)
        self.browser.get(self.live_server_url+'/user/Test/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Overall user rating: 0.333', body)
    
    def test_login_page(self):
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(
            title='T1', page_type=post.SITE_FEEDBACK, user_id=test_user
        )
        
        # Jim directly accesses the login page, logs in, and is redirected home
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('teST', 'test') #Testing cAsE iNsEnSiTiVe login
        new_url = self.browser.current_url
        self.assertEqual(new_url, self.live_server_url+'/')

        # Jim goes back to the login page, but it says he's already logged in
        self.browser.get(self.live_server_url+'/accounts/login/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('You are already logged in', body)

    def test_user_type_change(self):
        # Jim logs in as Test and votes Up on a post
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(title='Test post',
                            page_type=post.SITE_FEEDBACK,
                            user_id=test_user
        )
        self.browser.get(self.live_server_url+'/accounts/login/')
        self.login_user('Test', 'test')
        self.browser.get(self.live_server_url+'/pages/site_feedback/')
        self.browser.find_element_by_link_text("Up").click()
        time.sleep(1)

        # The post shows than an ADMIN has voted up
        self.browser.get(self.live_server_url+'/pages/site_feedback/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn("Overall: 1.0", body)
        self.assertIn('Administrator', body)

        # Jim changes user type to TEACHER
        self.browser.get(self.live_server_url+'/user/Test')
        self.check_for_redirect_after_link_click('Change your account type',
                                                 '/user_type/change/$'
                                                 )
        self.browser.find_element_by_xpath("//select[@name='user_type']/option[text()='Teacher']").click()
        self.check_for_redirect_after_button_click('user_type_change_button',
                                                 '/user_type/change/done/'
                                                 )

        # Jim sees his user type and vote has been changed
        self.browser.get(self.live_server_url+'/pages/site_feedback/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn("Overall: 1.0", body)
        self.assertIn('Teacher', body)
        self.assertNotIn('Administrator', body)
    
    def test_mark_as_spam_links(self):
        test_user = get_user_model().objects.get(username='Test')
        post1 = post.objects.create(
             title='T1', page_type=post.PROBLEMS, user_id=test_user
        )

        # Jim visits the ideas page and only sees 'Mark as spam' once logged in
        self.browser.get(self.live_server_url+'/pages/problems/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Mark as spam', body)
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Mark as spam', body)

        # Jim marks the post as spam
        self.browser.find_element_by_link_text('Mark as spam').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Thanks', body)
        post_of_interest = post.objects.get(title='T1')
        self.assertEqual(1, post_of_interest.spam.count())
        self.assertEqual(1, post_of_interest.spam_count)

        # Jim marks the post as spam again -- but the values do not change
        self.browser.get(self.live_server_url+'/pages/problems/')
        self.browser.find_element_by_link_text('Mark as spam').click()
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Thanks', body)
        post_of_interest = post.objects.get(title='T1')
        self.assertEqual(1, post_of_interest.spam.count())
        self.assertEqual(1, post_of_interest.spam_count)

        # Jim tries to directly access the spam url & gets a 404.
        self.browser.get(self.live_server_url+'/post/spam/'+str(post1.id)+'/')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Not Found', body)
        self.browser.get(self.live_server_url+'/pages/problems/')

        # Jim marks the comment as spam
        self.browser.find_element_by_link_text('T1').click()
        self.browser.find_element_by_id('id_content').send_keys('A comment')
        self.browser.find_element_by_name('comment_button').click()
        spam_links = self.browser.find_elements_by_link_text('Mark as spam')
        spam_links[1].click() #0 is for post
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Thanks', body)
        comment_of_interest = comment.objects.get(content='A comment')
        self.assertEqual(1, comment_of_interest.spam.count())
        self.assertEqual(1, comment_of_interest.spam_count)

        # Jim marks the comment as spam again -- but nothing happens
        self.browser.get(self.browser.current_url)
        spam_links = self.browser.find_elements_by_link_text('Mark as spam')
        spam_links[1].click() #0 is for post
        time.sleep(1)
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Thanks', body)
        comment_of_interest = comment.objects.get(content='A comment')
        self.assertEqual(1, comment_of_interest.spam.count())
        self.assertEqual(1, comment_of_interest.spam_count)
    
    def test_comment_functionality_and_existance(self):
        test_user = get_user_model().objects.get(username='Test')
        post.objects.create(
            title='T1', page_type=post.PROBLEMS, user_id=test_user
        )
        post.objects.create(
            title='T2', page_type=post.PROBLEMS, user_id=test_user
        )

        # Jim clicks on the post w/o login and doesn't see the Comment button
        self.browser.get(self.live_server_url+'/pages/problems/')
        self.browser.find_element_by_link_text('T1').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Comments', body)
        self.assertIn('no comments', body)
        self.assertIn('login to comment', body)
        text_areas = self.browser.find_elements_by_tag_name('textarea')
        self.assertEqual(len(text_areas), 0)

        # Jim logs in and sees the appropriate text and a place to comment
        self.browser.find_element_by_link_text('Login').click()
        self.login_user('Test', 'test')
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Comments', body)
        self.assertIn('no comments', body)
        text_areas = self.browser.find_elements_by_tag_name('textarea')
        self.assertEqual(len(text_areas), 2) #Fake and real

        # 1: Jim enters a comment and sees it
        text_areas[1].send_keys('Comment 1')
        self.browser.find_element_by_name('comment_button').click()
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Comment 1', comment_display)
        self.assertIn('Test', comment_display)
        self.assertIn('Reply', comment_display)
        self.assertIn('Delete', comment_display)

        # 2: Jim replys to himself (poor Jim)
        self.browser.find_element_by_link_text('Reply').click()
        text_areas = self.browser.find_elements_by_tag_name('textarea')
        text_areas[2].send_keys('1.1') #3nd textarea appeared from reply click
        comment_buttons = self.browser.find_elements_by_name('comment_button')
        comment_buttons[1].click() #2nd button appeared from reply click

        # Jim doesn't see his reply, but the body says are 2 comments
        comment_display = self.browser.find_element_by_id('commenters').text
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Comment 1', comment_display)
        self.assertNotIn('1.1', comment_display)
        self.assertIn('Comments(2)', body)

        # Jim changes the dropdown to show all comments & sees his reply
        self.browser.find_element_by_name("show_dropdown").click()
        self.browser.find_element_by_link_text("All comments").click()
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('1.1', comment_display)

        # Jim changes the dropdown & his reply disappears
        self.browser.find_element_by_name("show_dropdown").click()
        self.browser.find_element_by_link_text("Only top-level comments").click()
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertNotIn('1.1', comment_display)

        # Jim clicks 'show replies' & his reply reappears
        self.browser.find_element_by_link_text("Show replies(1)").click()
        time.sleep(1)
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('1.1', comment_display)

        # Jim marks his post as spam and sees "Thanks" w/o page reloading
        spam = self.browser.find_elements_by_link_text('Mark as spam')
        spam[2].click()
        time.sleep(1)
        comment_display = self.browser.find_element_by_id('commenters').text
        self.assertIn('Thanks', comment_display)

        # 3: Jim comments again (not a reply)
        self.browser.find_element_by_id('id_content').send_keys('Comment 2')
        self.browser.find_element_by_name('comment_button').click()

        # Jim deletes his 1st comment, which deletes his 1st 2 comments
        deletes = self.browser.find_elements_by_link_text('Delete')
        self.assertEqual(len(deletes), 3) # 0 - Delete post, 1 - 1st comment
        deletes[1].click() # 2 - Recent comment (note: reply is hidden)
        self.browser.switch_to_alert().accept()

        # Only Jim's 3rd comment remains
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comment 1', body)
        self.assertIn('Comment 2', body)
        self.assertIn('Comments(1)', body)
        
        # Jim goes to the next post, & doesn't see his comment
        self.browser.find_element_by_link_text('Problems').click()
        self.browser.find_element_by_link_text('T2').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Comment 2', body)
        self.assertIn('no comments', body)

        # Jim tries to comment w/o entering text and just spaces
        self.browser.find_element_by_name('comment_button').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a comment', body)
        self.browser.find_element_by_id('id_content').send_keys('  ')
        self.browser.find_element_by_name('comment_button').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Please enter a valid comment', body)


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

