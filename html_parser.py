from cache_manager import CacheManager
from task import Task
from lxml import html

class DetailsParser:
	def __init__(self, cache: CacheManager, cache_description: CacheManager, cache_result: CacheManager):
		self.cache = cache
		self.cache_description = cache_description
		self.cache_result = cache_result

	def parse(self, tasks: list[Task]):
		ready_tasks = []
		for task in tasks:
			if self.cache_description.is_cached(task.result_name_md) and self.cache_description.is_cached(task.result_name_md):
				logger.info(f"Result files for '{task.name}' already done")
				break
			else:
				task_content = self.cache.load(task.cache_name_html)
				task_content = make_html_from_string(task_content)
				task.cache_description = try_extract_description(task_content)
				task.tags = try_extract_tags(task_content)
				ready_tasks.append(task)
		return ready_tasks

def make_html_from_string(content: str):
	assert content is not None
	return html.fromstring(content)

def try_extract_description(task_html: html.HtmlElement):
	description = task_html.xpath('//div[@class="elfjS"]')[0].text_content()
	return description

def try_extract_tags(task_html: html.HtmlElement):
	tags = [i.text_content() for i in task_html.xpath('//a[@target="_blank"]')]
	return (list(filter(None, tags)))
