import re
import urllib
# e.g : 127.0.0.1:8080:user:pass
def load_proxies(filepath):

	proxies = []
	line_enumerator = 1

	with open(filepath, 'r') as _file:
		for line in _file:

			line = line.rstrip().lstrip()

			if len(line.split(':')) == 2:
				proxies.append(line)

			elif len(line.split(':')) == 4:
				splited = line.split(':')
				proxy = splited[2] + ':' + splited[3] + '@' + splited[0] + ':' + splited[1]
				proxies.append(proxy)

			else:
				print('Invalid proxy on line %i' % (line_enumerator))
				exit()

			line_enumerator += 1

	return proxies

def get_language_code(country_code):
	if country_code:
		switcher = {
			'US':'lang_en',
			'DE':'lang_de',
			'FR':'lang_fr',
			'NL':'lang_nl'
			}
		return switcher.get(country_code, 'lang_en')
	else:
		return 'lang_en'


def get_google_engine(country_code):
	if country_code:
		switcher = {
			'US':'www.google.com',
			'FR':'www.google.fr',
			'NL':'www.google.nl',
			'DE':'www.google.de'
			}
		return switcher.get(country_code, 'www.google.com')
	else:
		return 'www.google.com'

def compute_url(query, language_code, engine, num_results, start_at=0, safe_search=False):

	if safe_search:
		safe_search = '&safe=Active'
	else:
		safe_search = ''

	if start_at == 0:
		start_at = ''
	else:
		start_at = '&start=' + str(start_at)

	url = 'https://{0}/search?q={1}&btnG=Search&num={2}&lr={3}{4}{5}' \
                .format(engine, urllib.parse.quote(query), num_results, language_code, safe_search, start_at)

	return url

def check_for_malicious(response):

	if 'captcha' in response.text:
		return True
	else:
		return False

def gen_queries(operators_filepath, keywords_filepath, filters_filepath):

	operators, keywords, filters = [],[],[]

	queries = []

	with open(operators_filepath, 'r') as _file:
		for line in _file:
			operators.append(line.rstrip().lstrip())

	with open(keywords_filepath, 'r') as _file:
		for line in _file:
			keywords.append(line.rstrip().lstrip())

	with open(filters_filepath, 'r') as _file:
		for line in _file:
			filters.append(line.rstrip().lstrip())


	for operator in operators:
		for keyword in keywords:
			for filter in filters:
				queries.append(str(operator + keyword + ' ' + filter))

	return queries

def save_links(links, filepath):

	with open(filepath, 'a') as _file:
		for link in links:
			_file.write(link + '\n')

def save_burned(proxy, filepath):

	with open(filepath, 'a') as _file:
		_file.write(proxy + '\n')













