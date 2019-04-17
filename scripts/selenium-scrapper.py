from selenium import webdriver

class AprenderScrapper:
	'''
	'''
	def __init__(self, username, password):
		self.driver = webdriver.Firefox()
		self.username = username
		self.password = password
	def login(self):
		'''
		'''
		browser.get('https://aprender.unb.br/index.php')
		username = browser.find_element_by_id("login5")
		password = browser.find_element_by_id("password")
		username.send_keys(self.username)
		password.send_keys(self.password)
		browser.find_element_by_id("login8").click()

	def select_course(browser)
