#import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_home_page_has_proper_content_and_links(self):
        # Jim visits the home page of our site
        self.browser.get(self.live_server_url)

        # In the title are the words "Welcome To" and the word "Welcome" is
        # displayed on the page
        self.assertIn("Welcome To", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome', header_text)

        # Jim clicks on "Problems" link and is redirect to the problems page
        self.browser.find_element_by_link_text("Problems").click()
        self.browser.implicitly_wait(3)
        problems_url = self.browser.current_url
        self.assertRegexpMatches(problems_url, '/problems/$')

        
#    def test_problems_page_posts_and_saves_content(self):
        # The title of the problems page contains "Problems - "
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

    def test_user_creation_and_authorization(self):
        # Jim visits the homepage of the site (assume Jim is a user on the site)
        self.browser.get(self.live_server_url)

        # Jim sees a place to enter in his username and password
        login_box= self.browser.find_element_by_id('id_login_box').text
        self.assertIn('Username:', login_box)
        self.assertIn('Password:', login_box)

        # Jim enters his username and password into the appropriate boxes
        inputs = self.browser.find_elements_by_tag_name('input')
        inputs[0].send_keys('Jim')
        inputs[1].send_keys('Password')

        # Jim clicks the 'Login' button and is returned to the current page
        self.browser.find_element_by_link_text("Login").click()
        self.browser.implicitly_wait(3)
        home_url = self.browser.current_url
        self.assertRegexpMatches(home_url, '/$')
