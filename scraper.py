from Scraper.identity_manager import Identity, generate_identities
from Scraper.sync_http import get_request
from Scraper.utils import load_proxies, check_for_malicious, gen_queries, save_links, save_burned
from Scraper.google_search import GoogleSearch
from Scraper.parsing import parse_google_results, parse_google_pages
import logging
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p','--proxies', type=str, action='store', default='proxies.txt',
					help='Specify the name of the proxies file. Default : proxies.txt')
parser.add_argument('-b','--burned', type=str, action='store', default='burned.txt',
					help='Specify the name of the file where burned proxies are stored. Default : burned.txt')
parser.add_argument('-out','--output-file', type=str, action='store', default='output.txt',
					help='Specify the name of the output file. Default : output.txt')
parser.add_argument('-ope','--operators', type=str, action='store', default='operators.txt',
					help='Specify the name of the operators file. Default : operators.txt')
parser.add_argument('-k','--keywords', type=str, action='store', default='keywords.txt',
					help='Specify the name of the keywords file. Default : keywords.txt')
parser.add_argument('-f','--filters', type=str, action='store', default='filters.txt',
					help='Specify the name of the filters file. Default : filters.txt')
parser.add_argument('-n','--num-results-per-page', dest='num_results', type=int, action='store', default=50,
					help='Specify the number of results per page. (min. 10, max. 100) Default : 50')
parser.add_argument('-d','--depth', type=int, action='store', default=3,
					help='Specify the number of pages to search per query. Default : 3')
parser.add_argument('-c','--country', type=str, action='store', default='FR',
					help='Specify the country/lang to scrape Google. (only support FR, US, DE, NL) Default : FR')
parser.add_argument('-v','--verbose', action='store_true', default=False,
					help='Specify if scraper displays information while running. Default : False')


args = parser.parse_args()

if args.verbose:
	logging.basicConfig(level=logging.INFO)

print(args)

logging.info('Loading proxies from textfile.')
proxies = load_proxies(args.proxies)
logging.info('%i proxies loaded.', len(proxies))

logging.info('Generating identities.')
identities = generate_identities(proxies)
logging.info('%i identities generated', len(identities))

logging.info('Generating queries based on operators, keywords and filters.')
queries = gen_queries('operators.txt', 'keywords.txt', 'filters.txt')
logging.info('%i queries generated.', len(queries))

logging.info('Instantiating Scraper.')
google_search = GoogleSearch(identities, args.country, args.num_results)
logging.info('Scraper instantiated, engine : %s, language code : %s, number of results : %i', google_search.engine, google_search.language_code, google_search.num_results)


pages_depth = args.depth

logging.info('Starting queries.')
for query in queries:
	logging.info('Querying Google for %s', query)

	query_flag = False
	start_at = 0

	logging.info('Above first while : %i', start_at)
	while not query_flag:
		logging.info('Under first while : %i', start_at)

		tries = 0 # max tries = 3
		response_flag = False

		logging.info('Above second while : %i', start_at)
		while not response_flag and tries < 3:
			logging.info('Under second while : %i', start_at)

			response = google_search.search(query, start_at)

			logging.info('Checking for malicious request.')
			if check_for_malicious(response):
				burned = str(google_search.identities[google_search.identity_cursor].proxy)
				save_burned(burned, args.burned)
				print('Malicious request detected for proxy : ' + burned)
				if google_search.remove_burned_identity:
					logging.info('Removing burned identity.')
					google_search.pop_identity()
			else:
				logging.info('Extracting links from SERP.')
				links = parse_google_results(response.text)
				logging.info('Found %i links with number of results sets to %i ', len(links), google_search.num_results)
				
				response_flag = True

				logging.info('Saving links to file.')
				save_links(links, 'output.txt')

				if len(links) < (google_search.num_results - 5):
					logging.info('Reached last page of SERPs.')
					query_flag = True
				elif ((start_at + google_search.num_results) / google_search.num_results) == pages_depth:
					logging.info('Reached maximum depth for SERPs.')
					query_flag = True
				else:
					start_at = start_at + google_search.num_results

				links[:] = []

				
				logging.info('Shifting identity.')
				google_search.shift_identity()

			tries += 1
			if tries >= 3:
				logging.info('Exceded maximum number of retries for url.')
				query_flag = True

print('Done...')