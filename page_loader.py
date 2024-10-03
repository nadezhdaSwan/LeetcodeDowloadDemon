from cache_manager import CacheManager
from task import Task
from typing import List
import random, time
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions


import logging
logger = logging.getLogger(__name__)

def wait_for_delay(delay: int):
	logger.info(f"Waiting {delay} sec...")
	time.sleep(delay)

def assert_page_content(driver: webdriver.firefox.webdriver):
	count = 20 # задержка
	text = None
	while count and text == None:
		try:
			#text = driver.find_element(By.CLASS_NAME, "elfjS").text
			element = driver.find_element(By.XPATH, "//div[contains(text(), 'Topics')]")
			element.click()
			text = element.text

		except NoSuchElementException:
			time.sleep(1)
			count -= 1


	time.sleep(3)
	if not count:
		logger.warning(f"Don't have content")
	return count # если осталось время задержки
		



class PageLoader:
	def __init__(self, cache: CacheManager, min_delay: int, max_delay: int):
		self.cache = cache
		self.min_delay = min_delay
		self.max_delay = max_delay

	def download(self, tasks: List[Task]):
		count = 1
		total = len(tasks)
		for task in tasks:
			logger.info(f'{count}/{total}')
			count += 1
			if self.try_dowload_task_page(task):
				delay = random.randint(self.min_delay, self.max_delay)
				wait_for_delay(delay) 

	def try_dowload_task_page(self, task:Task) -> bool:
		logger.info(f'Downloading task from "{task.url}"')
		if self.cache.is_cached(task.cache_name_html):
			logger.info('Already in cache, skipping.')
			return False
		else:
			page = self.download_book_selenium(task)
			if page:
				self.cache.save(task.cache_name_html, page)
				return True
			else:
				return False

	def download_book_selenium(self, task:Task):
		logger.info(f'Start direct download page from "{task.url}"')
		opts = FirefoxOptions()
		opts.add_argument("--headless") # don't launch firefox window
		driver = webdriver.Firefox(options=opts)
		driver.get(task.url)
		content = False
		if assert_page_content(driver):
			content = driver.page_source
		driver.close()
		return content


	def download_book_page_direct(self, task:Task):
		logger.info(f'Start direct download page from "{task.url}"')
		headers = { \
#curl 'https://leetcode.com/problems/uncommon-words-from-two-sentences/description/' 
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', \
'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', \
'cache-control': 'no-cache', \
#  -H 'cookie: gr_user_id=8ecb8c97-28b3-4d7a-bfde-2a0b4fbd2092; 87b5a3c3f1a55520_gr_last_sent_cs1=b4HipfXExQ; __stripe_mid=c66ae725-4eaf-45df-9beb-2409b2e63246ccb2f6; cf_clearance=4jlTonuk.pSzMh.RzoZU12mnPh3tmQ_KYFYCTv3cmqI-1726125022-1.2.1.1-9_EpMKvQ9MC55OE_RSdq1JXAjNN633ZBQJwlmxzUuNqvcnSicIW4sql8TcpKRAokazv2w9S2hcoaiqGltWab9u9qPZ2d0GODXSuIz2iTWeKnSC83Y9dT6.qC2ROAxJgcYS1PBjFOEG6CFQyhRo3PGMwztz2hh.dMQZgzLHDaE3ezdwvqB1cgMxpDpJUCiG2UfYhxEH78vtte4KdiFoKzLRahAnRytQc1GnBcpd0jfEsQEPz6vI.QKFt7jQd.52x4_2F3rP_1VhqkZmEnn6d32_k4fv8Xy9lthhZzfHnrDfRDaav66HvLOULKDvITkd1g8uo1rxVB7rIvyap716jLiBjqqKeTiS3PVds1dKiP8sNLb1QXaVES2FuyV7cRO96SlUsuNemSSozS2_p2GEU8nfWcEdkznktB90j9UNag4Sg; csrftoken=eS9e9kdfZgVsnDLVQBlf1MuzmkFLIYqQoYi5Hab5gkqBfbnFDKJVfn1tKXQGdHr6; _gid=GA1.2.1793537584.1726402625; INGRESSCOOKIE=aa8e9bafae60c1c30612290513894307|8e0876c7c1464cc0ac96bc2edceabd27; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTQ3ODM1ODYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmZWRkMTg4YjQ1MDJlMDQwY2MyNzhlNDQ0OWViZDZjZjIwZmY1MGNlZjk1YmRhYzAyNzA2MWY1ZGM2MWFiNTk0IiwiaWQiOjE0NzgzNTg2LCJlbWFpbCI6Im5hbGViZWRldmF3b3JrQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYjRIaXBmWEV4USIsInVzZXJfc2x1ZyI6ImI0SGlwZlhFeFEiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYjRIaXBmWEV4US9hdmF0YXJfMTcyNjA2NzY0Ny5wbmciLCJyZWZyZXNoZWRfYXQiOjE3MjY4MTYzMzAsImlwIjoiOTEuMjQ3LjM3LjM3IiwiaWRlbnRpdHkiOiJiNzhiNGUyZDZjMGEzNjJjNDE4YjE0NWZlNDRlZDczZiIsInNlc3Npb25faWQiOjcyMTE4MTg5LCJkZXZpY2Vfd2l0aF9pcCI6WyJmZGY5MDMyOTMyZjAzNjExOWMwZDVkYzY3MzBjNDFiYSIsIjkxLjI0Ny4zNy4zNyJdfQ.WBZQPo1CZBVm5K9GtamfBcQjAkVUjNcFqCoagfOimJ0; __gads=ID=66afd9d58c7eb4e3:T=1726069180:RT=1726821621:S=ALNI_MaKJETcFwEIKEi81zWUkTIZsPaF5g; __gpi=UID=00000ee6098b553e:T=1726069180:RT=1726821621:S=ALNI_MZCHJ-VGRt6BYozIAkmgQSBuNKn2w; __eoi=ID=8b394b146a22c521:T=1726069180:RT=1726821621:S=AA-AfjYEbi4QT9gOqj04izKfWcR7; FCNEC=%5B%5B%22AKsRol8sjYACGHfM4BuQW0uPIV5vYXOtC9YJ8GJEQxDPE5mZ28TreY6RNZcZD3G2v7QwrWeJdVBDnVsODVTPrvKgkHrA3Z1uSvnMybm-zMrA0ib0_V5RT_ng7iAPh0MEtK5omK1bR6JsChnrc5yEjPK6X57YGaQyeg%3D%3D%22%5D%5D; ip_check=(false, "91.247.37.37"); 87b5a3c3f1a55520_gr_session_id=0333f24d-01d8-4200-b1ef-7a2f0144a593; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=0333f24d-01d8-4200-b1ef-7a2f0144a593; 87b5a3c3f1a55520_gr_session_id_sent_vst=0333f24d-01d8-4200-b1ef-7a2f0144a593; __cf_bm=E.qrX29Oj2JH9OreubcdXitWa1x9env157xETGvUE1Q-1726839488-1.0.1.1-kkqfeM4jGnn8BoxvNRQBNwfRZZp__jAk45DupiZXG5qJYbblT7LuoLHfe1GzKn4gyKDEtx1ZiF_jBFFN4AgRjA; 87b5a3c3f1a55520_gr_cs1=b4HipfXExQ; _ga=GA1.1.1416200160.1726069088; _ga_CDRWKZTDEX=GS1.1.1726838377.28.1.1726839638.60.0.0' \
'pragma': 'no-cache', \
'priority': 'u=0, i', \
'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', \
'sec-ch-ua-arch': "x86", \
'sec-ch-ua-bitness': "64", \
'sec-ch-ua-full-version': "124.0.6367.60",\
'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.60", "Google Chrome";v="124.0.6367.60", "Not-A.Brand";v="99.0.0.0"', \
'sec-ch-ua-mobile': '?0', \
'sec-ch-ua-model': "", \
'sec-ch-ua-platform': "Linux", \
'sec-ch-ua-platform-version': "6.8.0", \
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1', \
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
		}
		req = Request(task.url, headers = headers)
		r = urlopen(req)
		
		with r as data:
			content: bytes = data.read()
			#assert_page_content(content)
			logger.info('Page downloaded.')
			return content
