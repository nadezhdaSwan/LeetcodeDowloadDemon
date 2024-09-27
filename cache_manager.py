from pathlib import Path

import logging
logger = logging.getLogger(__name__)

class CacheManager:
	def __init__(self, cache_dir: Path):
		self.cache_dir = Path(cache_dir)
		self.ensure_cache_dir()

	def ensure_cache_dir(self):
		self.cache_dir.mkdir(parents=True, exist_ok=True)

	def get_path(self, name: str) -> str:
		return self.cache_dir / f'{name}.html'

	def is_cached(self, name: str) -> bool:
		return self.get_path(name).exists()

	def save(self, name: str, content: str):
		file_name = self.get_path(name)
		with open(file_name, 'w') as file:
			logger.info(f'Save to cache: "{file_name}"')
			file.write(content)

	def load(self, name: str):
		file_name = self.get_path(name)
		try:
			with open(file_name, 'r', encoding="utf-8") as file:
				return file.read()
		except Exception as ex:
			logger.info('load_book_content_from_cache("{file_name}"): {ex}')
			return None