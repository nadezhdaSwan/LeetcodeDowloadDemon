import time

class Task:
	def __init__(self, name: str, last_modified: time, created: time):
		self.name = name
		self.url = f'https://leetcode.com/problems/{self.name}/description/'
		self.cache_name_html = f'{self.name}.html'
		self.result_name_md = f'{self.name}.md'
		self.last_modified = last_modified
		self.created = created
		self.description = ''
		self.tags = []

	def create_result(self):
		tags = ['#'+tag.lower().replace(' ','-') for tag in self.tags]
		return f'''---
code: "[[leetcode/code/{self.name}.py]]"
url: {self.url}
tags:
  - leetcode
created: {time.strftime("%Y-%m-%d", self.created)}
---
descript_tags:: {', '.join(tags)}
![[leetcode/description/{self.result_name_md}]]
'''
