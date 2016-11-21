from bs4 import BeautifulSoup
import re
import urllib


def parse_google_results(response_text):

	links = []
	# pattern = re.compile('a href=\"\/url\?q=[a-zA-Z0-9:/.%-_]+[&amp;]?')
	pattern = re.compile('<a href="http[s]?:\/\/[a-zA-Z0-9-./]+[&amp;]?"')

	soup = BeautifulSoup(response_text, 'lxml')

	all_h3 = soup.find_all('h3')

	if len(all_h3) < 1:
		print('No H3 found !')
		exit()

	for h3 in all_h3:
		match = re.search(pattern, str(h3))
		if match:
			link = match.group(0).split('=')[1]
			link = link.split('&amp;')[0]
			link = link.replace('"','')
			links.append(urllib.parse.unquote(link))

	return links

def parse_google_pages(response_text):

	pattern = re.compile('<a aria-label="[a-zA-Z0-9 ]+" class="fl" href="[a-zA-Z0-9 ?\/:=;%_\-&+]+">')

	pages_url = []

	soup = BeautifulSoup(response_text, 'lxml')

	all_a_fl = soup.find_all('a', {'class':'fl'})
	print(len(all_a_fl))
	for a_fl in all_a_fl:
		match = re.search(pattern, str(a_fl))
		if match:
			pages_url.append(match.group(0))

	return pages_url


