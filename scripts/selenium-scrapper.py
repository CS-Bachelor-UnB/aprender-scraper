import re
from selenium import webdriver
from bs4 import BeautifulSoup

class AprenderScrapper:
	'''
	'''
	def __init__(self, username, password):
		self.browser = webdriver.Firefox()
		self.username = username
		self.password = password

	def login(self):
		'''
		'''
		self.browser.get('https://aprender.unb.br/index.php')
		username = browser.find_element_by_id("login5")
		password = browser.find_element_by_id("password")
		username.send_keys(self.username)
		password.send_keys(self.password)
		self.browser.find_element_by_id("login8").click()

	def select_course(self, course):
		'''
		'''
		course_list = self.browser.find_element_by_id('frontpage-course-list')
		soup_courselist = BeautifulSoup(course_list.get_attribute('innerHTML'))
		for div in soup_courselist.find_all('div', class_='coursebox'): 
			if re.search(course, div.div.h3.a.get_text().lower()) != None:
				browser.find_element_by_id(div.div.h3.a.get('id')).click()
				break

	def select_activity(self, activity):
		'''
		'''
		activity_list = self.browser.find_element_by_id('region-main')
		soup_activitylist = BeautifulSoup(activity_list.get_attribute('innerHTML'))
		for div in soup_activitylist.find_all('div', class_='activityinstance'):
			if re.search(activity, div.span.get_text().lower()) != None:
				self.browser.get(div.a.get('href'))
