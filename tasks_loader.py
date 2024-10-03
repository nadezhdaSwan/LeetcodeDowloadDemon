import os, time
import logging
from pathlib import Path
from typing import List
from task import Task

logger = logging.getLogger(__name__)

class TaskLoader:
	def load_from_dir(self, dir_: Path) -> List[Task]:
		if os.path.isdir(dir_):
			tasks = []
			for script_file in os.scandir(dir_):
				if script_file.is_file() and script_file.name.endswith('.py'):
					last_modified = time.gmtime(os.path.getmtime(dir_/script_file.name))
					created = time.gmtime(os.path.getctime(dir_/script_file.name))
					tasks.append(Task(script_file.name[:-3], last_modified, created))
				else:
					logger.warning(f"Foreign file or path '{script_file.name}'")
			logger.info(f"Imported tasks: {len(tasks)}")
			return tasks

		else:
			logger.error(f"Directory '{dir_}' do not exist")
			exit(1)			
			