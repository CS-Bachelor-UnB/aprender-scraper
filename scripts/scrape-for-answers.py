import re
from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.error
from http.cookiejar import CookieJar

 # Store the cookies and create an opener that will hold them
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('user-agent', 'logintest')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib.request.install_opener(opener)

# The action/ target from the form
authentication_url = 'https://aprender.ead.unb.br/login/index.php'

payload = {'username': '03641424135','password': 'Romulo.19'}

# Use urllib to encode the payload
data = urllib.parse.urlencode(payload).encode("utf-8")
req = urllib.request.Request(authentication_url, data)
with urllib.request.urlopen(req) as resp:
	contents = resp.read().decode('utf-8')
soup_userhome = BeautifulSoup(contents, 'html.parser')

# find all courses that I am enrolled in
courses = soup_userhome.find_all('div', class_='courses')

# get the page for a specific course - TESTING
for div in courses.find_all('div', class_='coursebox'):
	if re.search('projeto e analise de algoritmos', div.h3.a.get_text().lower()) != None:
		url_coursehome = div.h3.a.get('href')
		break
soup_coursehome = BeautifulSoup(urllib.request.urlopen(url_coursehome), 'html.parser')

# get the soup for the current or target week (in the future, have the current week automatically check)
courseweeks = soup_coursehome.find('ul', class_='weeks')
for li in courseweeks.find_all('li'):
	if re.search('9 abril', str(li.get('aria-label')).lower()) != None:
		soup_courseweek = li
		break

# get the page for a specific activity
for link in soup_courseweek.find_all('a'):
	if re.search('metodo iteração', link.get_text().lower()) != None:
		url_activityhome = link.get('href')
		break
soup_activityhome = BeautifulSoup(urllib.request.urlopen(url_activityhome), 'html.parser')

# submit payload to request activity (payload must be extracted from page)
payload = []
url_activity = soup_activityhome.find('form').get('action')
for field in soup_activityhome.find('form').find_all('input', type='hidden'):
	payload.append((field.get('name'), field.get('value')))
data = urllib.parse.urlencode(dict(payload)).encode("utf-8")
with urllib.request.urlopen(urllib.request.Request(url_activity, data)) as resp: 
	soup_activitypage = BeautifulSoup(resp.read().decode('utf-8'))

