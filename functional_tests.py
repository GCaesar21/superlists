from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import unittest

class NewVisitorTest(unittest.TestCase):   


	def setUp(self):
		options = Options()
		options.binary_location = r"D:\Program Files\Mozilla Firefox/firefox.exe"
		service = Service(executable_path=r"D:/Python/Scripts/geckodriver.exe")
		self.browser = webdriver.Firefox(service=service, options=options)

	def tearDown(self):
		self.browser.quit()
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')
		self.browser.implicitly_wait(10)
		self.assertIn('To-do',self.browser.title)
		self.fail('Finish the test!')


if __name__=='__main__':
	unittest.main(warnings='ignore')
#assert 'successfully' in browser.title, "Browser title was " +browser.title
