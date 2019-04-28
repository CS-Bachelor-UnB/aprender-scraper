import re, getpass
from selenium import webdriver
from bs4 import BeautifulSoup

class AprenderScrapper:
	'''
	'''
	def __init__(self):
		self.browser = webdriver.Firefox()
		self.username = ''
		self.password = ''

		# logs into the user's Aprender homepage
		self.homepage = self.__login()
		self.coursepage = self.select_course()
		self.activitypage = self.select_activity()

	def __login(self, username='03641424135', password='Romulo.19'):
		'''
		'''
		if not username or not password:
			self.username = input('Username: ')
			self.password = getpass.getpass('Password: ')
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
		
		return BeautifulSoup(self.browser.page_source, 'html.parser')

	def select_course(self, course=''):
		'''
		Selects course from course list on user's homepage
		Args:
			+ string contained in the course name.
			  if no string is given, it takes the first course it finds
		Retruns:
			+ BeautifulSoup object for the course homepage if selected course is clicked on, empty object otherwise
		'''
		soup_courselist = BeautifulSoup(self.browser.find_element_by_id('frontpage-course-list').get_attribute('innerHTML'), 'html.parser')
		if course:
			for h3 in soup_courselist.find_all('h3'):
				if course in h3.a.get_text().lower():
					self.browser.find_element_by_link_text(h3.a.get_text()).click()
					return BeautifulSoup(self.browser.page_source, 'html.parser')

			return BeautifulSoup('')

		else:
			index = 0
			courses = []
			for h3 in soup_courselist.find_all('h3'):
				print(index, h3.a.get_text())
				courses.append(h3.a.get_text())
				index += 1

			choice = input('Select a number: ')
			try:
				self.browser.find_element_by_link_text(courses[int(choice)]).click()

			except Exception as e:
				print('select_course()\tcourse: ', course, e )
				return BeautifulSoup('')

			else:
				return BeautifulSoup(self.browser.page_source, 'html.parser')			

	def select_activity(self, activity=''):
		'''

		'''
		soup_activitylist = BeautifulSoup(self.browser.find_element_by_id('region-main').get_attribute('innerHTML'), 'html.parser')
		if activity:
			for div in soup_activitylist.find_all('div', class_='activityinstance'):
				if activity in div.a.get_text().lower():
					self.browser.get(div.a.get('href'))
					return BeautifulSoup(self.browser.page_source, 'html.parser')
					
			return BeautifulSoup('')

		else:
			index = 0
			activities = []
			for div in soup_activitylist.find_all('div', class_='activityinstance'):
				print(index, div.a.get_text())
				activities.append(div.a.get('href'))
				index += 1

			choice = input('Select a number: ')
			try:
				self.browser.get(activities[int(choice)])
				# self.browser.get(div.a.get('href'))

			except Exception as e:
				print('select_activity()\tactivity: ', activity, e )
				return BeautifulSoup('')

			else:
				return BeautifulSoup(self.browser.page_source, 'html.parser')

	def back(self):
		'''
		'''
		try:
			self.browser.back()
			return True
		
		except Exception as e:
			print(e)
			return False
	
	def forward(self):
		'''
		'''
		try:
			self.browser.forward()
			return True
		
		except Exception as e:
			print(e)
			return False

	def open_scorm_activity(self):
		'''
		Work in progess
		'''
		self.browser.find_element_by_xpath("//input[@type='submit']").click()

		# switch to iframe and show all questions
		self.browser.switch_to.frame(self.browser.find_element_by_tag_name("iframe"))
		self.browser.find_element_by_id('ShowMethodButton').click()
		return BeautifulSoup(self.browser.page_source, 'html.parser')