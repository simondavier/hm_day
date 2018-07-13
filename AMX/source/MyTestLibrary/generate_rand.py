# -*- coding: utf-8 -*-
import random

class Generate_random(object):
	"""docstring for Generate_random"""

	def __init_(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
	
	def generate(self,arg):
		u'''
		use to generate random list.  eg:
		|generate | arg |
		'''
		arg = int(arg)
		list = []
		listsample = []
		list_res=[]
		for i in range(1,arg):
			list.append(i)
		step = random.randint(1,arg)
		if step<arg:
			listsample = random.sample(list,step)
			listsample.sort()
			list_res=map(str,listsample)
			str1 = ','.join(list_res)
			return str1
		else:
			list_res=map(str,list)
			str2 = ','.join(list_res)
			return str2

if __name__ == '__main__':
	g = Generate_random()
	result = g.generate("9")
	print result
