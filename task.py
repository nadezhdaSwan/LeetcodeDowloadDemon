class Task:
	def __init__(self, name: str):
		self.name = name
		self.url = f'https://leetcode.com/problems/{self.name}/description/'
		self.cache_name_html = f'{self.name}.html'
		self.result_name_md = f'{self.name}.md'
		self.description = ''
		self.tags = []
