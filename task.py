class Task:
	def __init__(self, name: str):
		self.name = name
		self.url = f'https://leetcode.com/problems/{self.name}/description/'
