import re, os, getpass
from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.error
from http.cookiejar import CookieJar

class AprenderScraper:
	'''
	'''
	def __init__(self, course='', activity=''):
		'''
		Returns reference to new AprenderScraper object
		'''
		self.username = ''
		self.password = ''
		self.cookiejar = CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
		urllib.request.install_opener(self.opener)

		# requests user homepage
		self.userhome = self._authenticate()

		# requests course homepage if argument provided in the constructor
		if course:
			self.coursehome = self.select_course(self.userhome, course)
		else:
			self.coursehome = ''

		# requests activity page if argument provided in the constructor
		if activity:
			self.activitypage = self.select_activity(self.coursehome, activity)
		else:
			self.activitypage = ''


	def _authenticate(self, username='', password=''):
		'''
		Logs in to the account and returns a BeautifulSoup object with the html data for the homescreen
		'''
		# requests username if none provided
		if not username and not self.username:
			self.username = input('Username (CPF): ')
		else:
			self.username = username

		# requests password if none provided
		if not password and not self.password:
			self.password = getpass.getpass('Password: ')
		else:
			self.password = password

		# authenticate and return BeautifulSoup object of the user's homepage
		authentication_url = 'https://aprender.ead.unb.br/login/index.php'
		payload = {'username': self.username,'password': self.password}
		data = urllib.parse.urlencode(payload).encode("utf-8")
		with urllib.request.urlopen(urllib.request.Request(authentication_url, data)) as resp:
			return BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')


	def select_course(self, soup, course=''):
		'''
		Receives an user's BeautifulSoup homepage object and return the equivalent object
		for the course homepage
		'''
		# requests user input for course if none provided
		if not course:
			course = input('Name or tag of course: ')

		# gets a list of all courses listed on the user's homepage
		courses = []
		for div in soup.find_all('div', class_='coursebox'):
			courses.append(div.h3.a.get_text)
			if re.search(course, div.h3.a.get_text().lower()) != None:
				url_coursehome = div.h3.a.get('href')
				break

		if not url_coursehome:
			print('Course {} not found. Courses found: {}'.format(course, courses))
			return  ''

		return  BeautifulSoup(urllib.request.urlopen(url_coursehome), 'html.parser')


	def select_activity(self, soup, activity=''):
		'''
		Receives a course's homepage soup and returns an activity's homepage
		'''
		# requests user input for activity if none provided
		if not activity:
			activity = input('Name or tag for activity: ')

		for div in soup.find_all('div', class_='activityinstance'):
			if re.search(activity, div.span.get_text().lower()) != None:
				return BeautifulSoup(urllib.request.urlopen(div.a.get('href')), 'html.parser')


	def open_activity(self, soup):
		'''
		Receives an activity's homepage and opens it
		Returns a BeautifulSoup object for the activity page 
		'''
		# submits payload to request activity (payload must be extracted from page)
		payload = []
		url_activity = soup.find('form').get('action')
		for field in soup.find('form', id='scormviewform').find_all('input', type='hidden'):
			payload.append((field.get('name'), field.get('value')))
		data = urllib.parse.urlencode(dict(payload)).encode("utf-8")
		with urllib.request.urlopen(urllib.request.Request(url_activity, data)) as resp:
			return BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')

