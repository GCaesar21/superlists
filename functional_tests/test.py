from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
import time
import unittest
from selenium.common.exceptions import WebDriverException
MAX_WAIT=10

class NewVisitorTest(LiveServerTestCase):   
	options = Options()
	options.binary_location = r"D:\Program Files\Mozilla Firefox/firefox.exe"
	#service = Service(executable_path=r"D:/Python/Scripts/geckodriver.exe")

	def setUp(self):
		service = Service(executable_path=r"D:/Python/Scripts/geckodriver.exe")
		self.browser = webdriver.Firefox(service=service, options=self.options)

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self,row_text):
		start_time=time.time()
		while True:
			try:
				table=self.browser.find_element(by='id',value='id_list_table')
				rows=table.find_elements(by='tag name',value='tr')
				self.assertIn(row_text,[row.text for row in rows])
				return
			except (AssertionError,WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
			
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)
		self.browser.implicitly_wait(10)

		#The title and header of the website contain the word "To-Do"
		self.assertIn('To-Do',self.browser.title)
		#Locate the <h1> tag on the page and retrieve its text
		header_text=self.browser.find_element(by='tag name',value='h1').text
		self.assertIn('To-Do',header_text)

		#The app invites her to enter a to-do list

		#The verification page has an input box for entering the to-do items.
		inputbox=self.browser.find_element(by='id',value='id_new_item')
		#Verify that the placeholder text in the input box is correct.
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		#She typed "Buy peacock feathers" into the text field.
		#After pressing the Enter key, the page updates
		#the todo item she entered earlier shows "Buy peacock feathers."Press Enter to submit the item and wait 1 second for the page to refresh
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#Enter the second to-do item
		inputbox=self.browser.find_element(by='id',value='id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)

		time.sleep(1)

		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		self.wait_for_row_in_list_table('1: Buy peacock feathers')


		#A text box is displayed where you can enter additional items
		#self.fail('Finish the test!')


	def test_multiple_users_can_start_lists_at_different_urls(self):
	
		#The first user created a new to-do list.
		#And an item to do was added to it.
		self.browser.get(self.live_server_url)
		inputbox=self.browser.find_element(by='id',value='id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')

		#The first user notices that the list has a unique URL
		edith_list_url=self.browser.current_url
		self.assertRegex(edith_list_url,'/lists/.+')

		#The second user visits the website
		#Use a new browser session
		#Make sure that no information about the first user is leaked from the cookie
		self.browser.quit()
		new_service = Service(executable_path=r"D:/Python/Scripts/geckodriver.exe")
		self.browser = webdriver.Firefox(service=new_service, options=self.options)

		#
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element(by='tag name', value='body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertNotIn('make a fly',page_text)

		#
		inputbox=self.browser.find_element(by='id',value='id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		#
		francis_list_url=self.browser.current_url
		self.assertRegex(edith_list_url,'/lists/.+')
		self.assertNotEqual(francis_list_url,edith_list_url)

		#
		page_text=self.browser.find_element(by='tag name',value='body').text
		self.assertNotIn('Buy peacock feathers',page_text)
		self.assertIn('Buy milk',page_text)



#if __name__=='__main__':
#	unittest.main(warnings='ignore')
#assert 'successfully' in browser.title, "Browser title was " +browser.title
