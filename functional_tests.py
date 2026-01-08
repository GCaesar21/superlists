from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
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
		inputbox.send_keys('Buy peacock feathers')

		#After pressing the Enter key, the page updates
		#the todo item she entered earlier shows "Buy peacock feathers."

		#Press Enter to submit the item and wait 1 second for the page to refresh
		inputbox.send_keys(Keys.Enter)
		time.sleep(1)
		
		table=self.browser.find_element(by='id',value='id_list_table')
		rows=table.find_elements(by='tag name',value='tr')
		self.assertTrue(
			any(row.text=='1: Buy peacock feathers' for row in rows)
		)

		#A text box is displayed where you can enter additional items
		self.fail('Finish the test!')


if __name__=='__main__':
	unittest.main(warnings='ignore')
#assert 'successfully' in browser.title, "Browser title was " +browser.title
