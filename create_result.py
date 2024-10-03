from task import Task
from cache_manager import CacheManager

import logging
logger = logging.getLogger(__name__)

class Writer:
	def __init__(self, tasks: list[Task], cache_description: CacheManager, cache_result: CacheManager):
		self.tasks = tasks
		self.cache_description =cache_description
		self.cache_result=cache_result

	def save_result(self, ):
		for task in self.tasks:
			#print(task.description)
			self.cache_description.save(task.result_name_md,task.description)
			self.cache_result.save(task.result_name_md,task.create_result())





