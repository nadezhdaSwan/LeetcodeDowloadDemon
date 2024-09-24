import os
import logging
from pathlib import Path
from typing import List
from task import Task

logger = logging.getLogger(__name__)

class TaskLoader:
	def load_from_dir(self, dir_name: Path) -> List[Task]:
		if os.path.isdir(dir_name):
			tasks = []
			for script_file in os.scandir(dir_name):
				if script_file.is_file() and script_file.name.endswith('.py'):
					tasks.append(Task(script_file.name[:-3]))
				else:
					logger.warning(f"Foreign file or path '{script_file.name}'")
			logger.info(f"Imported tasks: {len(tasks)}")
			return tasks

		else:
			logger.error(f"Directory '{dir_name}' do not exist")
			exit(1)			
			