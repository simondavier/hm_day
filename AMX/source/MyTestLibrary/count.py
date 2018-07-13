# -*- coding: utf-8 -*-
class Count(object):
	"""docstring for ClassName"""
	def __init_(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
	
	def add(self, a, b):
		u'''
		use to sum a , b.  eg:
		| add | a  | b |
		'''
		return int(a) + int(b)

	def sub(self, a , b):
		u'''
		use to sum a , b.  eg:
		| add | a  | b |
		'''
		return int(a) - int(b)

if __name__ == '__main__':
	c = Count()
	result = c.add(2, 3)
	assert result==5
	result = c.sub(6, 3)
	assert result==3