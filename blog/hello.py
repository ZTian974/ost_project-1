#! /usr/bin/python

class HelloWorld():
	def __init__(self):
		self.words = ['Beijing','Chongqing','Shanghai']
		self.capitals = ['Beijing','WashtionDC','Berlin']

	def printword(self):
		for w in self.words:
			if w == 'Beijing':
				print 'Beijing is the capital of China'
			else:
				for c in self.capitals:
					if c == 'WashtionDC':
						print 'this is the capital of America'

if __name__ == '__main__':
	h = HelloWorld()
	h.printword()