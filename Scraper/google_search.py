import time
import logging
from Scraper.utils import get_language_code, get_google_engine, compute_url
from Scraper.sync_http import get_request

class GoogleSearch():

	def __init__(self, identities, country_code, num_results, remove_burned_identity=True):

		self.num_identities = len(identities)
		self.identities = identities
		self.remove_burned_identity = remove_burned_identity

		self.identity_cursor = 0
		self.last_loop_timestamp = int(time.time())

		self.num_results = num_results
		self.language_code = get_language_code(country_code)
		self.engine = get_google_engine(country_code)


	def search(self, query, start_at=0):

		url = compute_url(query, self.language_code, self.engine, self.num_results, start_at)
		logging.info('Requesting Google for url : %s', url)

		headers = self.identities[self.identity_cursor].headers
		proxy = {'http':self.identities[self.identity_cursor].proxy,
				 'https':self.identities[self.identity_cursor].proxy}

		return get_request(url, headers, proxy)

	def check_ip(self):
		headers = self.identities[self.identity_cursor].headers
		proxy = {'http':self.identities[self.identity_cursor].proxy,
				 'https':self.identities[self.identity_cursor].proxy}

		print(get_request('https://api.ipify.org?format=json', headers, proxy).text)


	def shift_identity(self):

		if (self.num_identities - self.identity_cursor) == 1:
			if (int(time.time() - self.last_loop_timestamp) < 30):
				time.sleep(int(time.time() - self.last_loop_timestamp))
			self.last_loop_timestamp = int(time.time())
			self.identity_cursor = 0
		else:
			self.identity_cursor += 1

	def pop_identity(self):

		if self.num_identities < 2:
			print('You have burned all your identities...exiting.')
			exit()

		burned_identity = self.identities.pop(self.identity_cursor)

		with open('burned_proxies.txt', 'w') as _file:
			_file.write(str(burned_identity.proxy) + '\n')

		self.num_identities = len(self.identities)



