from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r"D:\Program Files\Mozilla Firefox/firefox.exe"
service = Service(executable_path=r"D:/Python/Scripts/geckodriver.exe")


browser = webdriver.Firefox(service=service, options=options)
browser.get('http://localhost:8000')
browser.implicitly_wait(10)

assert 'successfully' in browser.title
