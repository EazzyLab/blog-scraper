from Scraper.user_agents import random_user_agent

class Identity():

	def __init__(self, user_agent, proxy):

		self.user_agent = user_agent
		self.proxy = proxy
		self.cookie = ''
		self.headers = {'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9,image/webp,*/*;q=0.8',
						'Accept-Encoding':'gzip, deflate, sdch',
						'Accept-Language':'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
						'User-Agent':self.user_agent,
						'Cookie':self.cookie}


def generate_identities(proxies):

	identities = [] # list of Identitiy

	for proxy in proxies:

		tmp_identity = Identity(random_user_agent(), proxy)
		identities.append(tmp_identity)

	return identities