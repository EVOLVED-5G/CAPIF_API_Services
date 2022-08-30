import yaml
import os

#Config class to get config
class Config:
	def __init__(self):
		self.cached = 0
		self.file="./config.yaml"
		self.config = {}
		stamp = os.stat(self.file).st_mtime
		if stamp != self.cached:
			self.cached = stamp
			f = open(self.file)
			self.config = yaml.safe_load(f)
			f.close()

	def getConfig(self):
		return self.config