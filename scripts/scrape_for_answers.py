import re, os
from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.error
from http.cookiejar import CookieJar

class AprenderScrapper:
	'''
	'''
	def __init__(self, username, password):
		'''
		Receives user data to for the scraping session
		Returns reference to i)self-object created, ii)user's homepage BeautifulSoup object 
		'''
		if not username and not password:
			os._exit(1)

		self.username = username
		self.password = password
		self.cookiejar = CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
		urllib.request.install_opener(self.opener)


	def _authenticate(self):
		'''
		Logs in to the account and returns a BeautifulSoup object with the html data for the homescreen
		'''
		authentication_url = 'https://aprender.ead.unb.br/login/index.php'
		payload = {'username': self.username,'password': self.password}
		data = urllib.parse.urlencode(payload).encode("utf-8")
		with urllib.request.urlopen(urllib.request.Request(authentication_url, data)) as resp:
			return BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')


	def select_course(self, soup):
		'''
		Receives an user's BeautifulSoup homepage object and return the equivalent object
		for the course homepage
		'''
		# requests user input for course
		course = input('Name or tag of course: ')

		# gets a list of all courses listed on the user's homepage
		for div in soup.find_all('div', class_='coursebox'):
			if re.search(course, div.h3.a.get_text().lower()) != None:
				url_coursehome = div.h3.a.get('href')
				break

		return  BeautifulSoup(urllib.request.urlopen(url_coursehome), 'html.parser')


	def select_activity(self, soup):
		'''
		Receives a course's homepage soup and returns an activity's homepage
		'''
		# requests user input for activity
		activity = input('Name or tag for activity: ')
		for div in soup.find_all('div', class_='activityinstance'):
			if re.search(activity, div.span.get_text().lower()) != None:
				return BeautifulSoup(urllib.request.urlopen(div.a.get('href')), 'html.parser')


	def open_activity(self, soup):
		'''
		Receives a course's homepage, selects activity and opens it 
		'''
		# requests the course homepage
		soup = self.select_course(soup)

		# requests the activity homepage
		soup = self.select_activity(soup)

		# submits payload to request activity (payload must be extracted from page)
		payload = []
		url_activity = soup.find('form').get('action')
		for field in soup.find('form', id='scormviewform').find_all('input', type='hidden'):
			payload.append((field.get('name'), field.get('value')))
		data = urllib.parse.urlencode(dict(payload)).encode("utf-8")
		with urllib.request.urlopen(urllib.request.Request(url_activity, data)) as resp:
			return BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
