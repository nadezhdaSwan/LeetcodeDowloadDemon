import logging
from pathlib import Path

from tasks_loader import TaskLoader
from cache_manager import CacheManager
from page_loader import PageLoader

#logger settings
logging.basicConfig(filename='leetcode.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#settings
code_dir = Path('result_obsidian/code')
cache_dir = Path('cache')
min_delay = 20
max_delay = 30

logger.info(f"Start load tasks from dir: '{code_dir}'")
tasks_loader = TaskLoader()
tasks = tasks_loader.load_from_dir(code_dir)
logger.info(f"Stop load tasks")

logger.info('Start download detailed task pages')
cache = CacheManager(cache_dir)
loader = PageLoader(cache, min_delay, max_delay)
loader.download(tasks)
logger.info('Stop load detailed task pages')


