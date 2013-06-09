import unittest
from selenium import webdriver

class NewVisitorTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_home_page_has_proper_content_and_links(self):
        # Jim visits the home page of our site
        self.browser.get('http://localhost:8000')

        # In the title are the words "Welcome To" and the word "Welcome" is
        # displayed on the page
        self.assertIn("Welcome To", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Welcome', header_text)

        # Jim clicks on "Problems" link and is redirect to the problems page

#    def test_problems_page_posts_and_saves_content(self):
        # The title of the problems page contains "Problems - "
        self.assertIn("Problems - ", self.browser.title)

        # A textarea is displayed, prompting "Type your thoughts here!"

        # Jim types in "School is bad, mkay?"

        # Jim presses enter and his post is displayed

        # Jim types "I good at school". Jim clicks the "Post" button

        # Both posts are displayed, and the textarea remains on the page
        # willing to handle more input



if __name__ == '__main__':
    unittest.main()
