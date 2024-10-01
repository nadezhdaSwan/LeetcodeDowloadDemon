import logging
from pathlib import Path

from tasks_loader import TaskLoader
from cache_manager import CacheManager
from page_loader import PageLoader
from html_parser import DetailsParser

#logger settings
logging.basicConfig(filename='leetcode.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#settings

cache_dir = Path('cache')
result_dir = Path('result_obsidian')
description_dir = result_dir / Path('description')
code_dir = result_dir / Path('code')
min_delay = 1
max_delay = 1

if __name__=='__main__':
	logger.info(f"Start load tasks from dir: '{code_dir}'")
	tasks_loader = TaskLoader()
	tasks = tasks_loader.load_from_dir(code_dir)
	logger.info(f"Stop load tasks")

	logger.info('Start download detailed task pages')
	cache = CacheManager(cache_dir)
	loader = PageLoader(cache, min_delay, max_delay)
	loader.download(tasks)
	logger.info('Stop load detailed task pages')

	logger.info('Prepare tasks for export.')
	cache_description = CacheManager(description_dir)
	cache_result = CacheManager(result_dir)
	details_parser = DetailsParser(cache, cache_description, cache_result)
	ready_tasks = details_parser.parse(tasks)
	logger.info(f'Tasks ready to export: {len(ready_tasks)}.')




