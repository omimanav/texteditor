from json import loads, dumps

class Userconfig:
	def __init__(self):
		self.file = open("config.json", "r")
		self.data = self.file.read()
		self.file.close()
		
	def get(self):
		return loads(str(self.data))
	
	def set(self, tabwidth, tabsize, fontspecs, theme):
		userconfig = {
			"tabwidth":tabwidth
			,"tabsize":tabsize
			,"fontspecs":list(fontspecs)
			,"theme":theme
		}
		self.file = open("config.json", "r")
		self.file.write(dumps(userconfig))
		self.file.close()