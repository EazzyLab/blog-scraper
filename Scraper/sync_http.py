import requests


def get_request(url, headers=None, proxy=None):

	r = requests.get(url, headers=headers, proxies=proxy)

	return r