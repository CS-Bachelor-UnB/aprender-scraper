import re
from selenium import webdriver
from bs4 import BeautifulSoup

class AprenderScrapper:
	'''
	'''
	def __init__(self):
		self.browser = webdriver.Firefox()
		self.username = ''
		self.password = ''

	def login(self, username='', password=''):
		'''
		'''
		if not username or not password:
			# request credentials
			self.username = input('Username: ')
			self.password = input('Password: ')
		else:
			self.username = username
			self.password = password

		# open Firefox
		self.browser.get('https://aprender.unb.br/index.php')

		# fill in credentials
		self.browser.find_element_by_id("login5").send_keys(self.username)
		self.browser.find_element_by_id("password").send_keys(self.password)

		# submit credentials
		self.browser.find_element_by_id("login8").click()

	def select_course(self, course):
		'''
		Needs finishing - click on course after activity is found
		'''
		course_list = self.browser.find_element_by_id('frontpage-course-list')
		soup_courselist = BeautifulSoup(course_list.get_attribute('innerHTML'), 'html.parser')
		for div in soup_courselist.find_all('div', class_='coursebox'): 
			if re.search(course, div.div.h3.a.get_text().lower()) != None:
				self.browser.find_element_by_id(div.div.h3.a.get('id')).click()
				break

	def select_activity(self, activity):
		'''
		Needs finishing - click on link after activity is found
		'''
		activity_list = self.browser.find_element_by_id('region-main')
		soup_activitylist = BeautifulSoup(activity_list.get_attribute('innerHTML'), 'html.parser')
		for div in soup_activitylist.find_all('div', class_='activityinstance'):
			if re.search(activity, div.span.get_text().lower()) != None:
				self.browser.get(div.a.get('href'))
