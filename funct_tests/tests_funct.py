# Stdlib imports

# Core Django imports
from django.test import LiveServerTestCase

# 3rd party imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# App imports


class NewVisitorTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
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
    
    def test_home_page_has_proper_content_and_links(self):
        # Jim visits the home page of our site
        self.browser.get(self.live_server_url)

        # In the title are the words "Welcome To" and the word "Welcome" is
        # displayed on the page
        self.assertIn("Welcome to ", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome', header_text)

        # Jim clicks on "Problems" link and is redirect to the problems page
        self.check_for_redirect_after_link_click("Problems", '/problems/$')
       
    def test_problems_page_posts_and_saves_content(self):
        # The title of the problems page contains "Problems - "
        self.browser.get(self.live_server_url+'/problems/')
        self.assertIn("Problems - ", self.browser.title)

        # A textarea is displayed, prompting "Type your thoughts here!"
        inputText = self.browser.find_element_by_id('id_new_post')
        self.assertEqual(
            inputText.get_attribute('placeholder'), 'Type your thoughts here!'
        )
        
        # Jim types in "School is bad, mkay?"
        inputText.send_keys('School is bad, mkay?')

        # Jim presses enter and his post is displayed
        inputText.send_keys(Keys.ENTER)
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', page_text)

        # Jim types "I good at school". Jim clicks the "Post" button
        inputText = self.browser.find_element_by_id('id_new_post')
        inputText.send_keys('I good at school')
        self.browser.find_element_by_id('id_post_button').click()

        # Both posts are displayed, and the textarea remains on the page
        # willing to handle more input
        page_text =  self.browser.find_element_by_tag_name('body').text
        self.assertIn('School is bad, mkay?', page_text)
        self.assertIn('I good at school', page_text)

    def test_user_login_existance_and_authorization(self):
        ######TODO - Update this test for authorization check
        ######TODO - test login_box appears on EVERY page

        # On the homepage, Jim sees a place to enter in his
        # username and password
        self.browser.get(self.live_server_url)
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Username:', login_box)
        self.assertIn('Password:', login_box)

        # Jim see enters his username and password into the appropriate boxes
        inputs = self.browser.find_elements_by_tag_name('input')
        self.assertEqual(len(inputs), 3)
        user = self.browser.find_element_by_id('id_user_login')
        password = self.browser.find_element_by_id('id_pass_login')
        user.send_keys('Jim')
        password.send_keys('Password')

        # Jim clicks the 'Login' button and is returned to the current page
        self.check_for_redirect_after_button_click("login",
                                                   self.live_server_url + '/$')

        # Jim now decides to try to login on the Problems page
        self.browser.get(self.live_server_url+'/problems/')
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Username:', login_box)
        self.assertIn('Password:', login_box)

        # Jim enters in his info, clicks 'Login', and is return to home page
        user = self.browser.find_element_by_id('id_user_login')
        password = self.browser.find_element_by_id('id_pass_login')
        user.send_keys('Jim')
        password.send_keys('Password')
        self.check_for_redirect_after_button_click("login",
                                                   self.live_server_url + '/$')
    
    def test_user_creation_form(self):
        ######TODO - Try incorrect passwords, improper email format
        ######TODO - username already taken, and check for verification email
        
        # On the homepage, Jim sees a place to create an account
        self.browser.get(self.live_server_url)
        login_box = self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Create Account', login_box)

        # Jim clicks the link and is redirected to a create account page
        self.check_for_redirect_after_link_click('Create Account',
                                                 '/accounts/register/$')

        # Jim sees 4 input boxes and a button
        inputs = self.browser.find_elements_by_tag_name('input')
        self.assertEqual(len(inputs), 9)
        
        # Jim enters in his information
        inputs[4].send_keys('Jim')
        inputs[5].send_keys('chipperdrew@gmail.com')
        inputs[6].send_keys('Password')
        inputs[7].send_keys('Password')

        # Jim presses the "Create" button and is returned to home page
        self.check_for_redirect_after_button_click("create",
                                                   self.live_server_url + '/$')
