from count import Count
from generate_rand import Generate_random

__Version__= '0.1'


class MyTestLibrary(Count,Generate_random):
	ROBOT_LIBRARY_SCOPE = 'GLOBAL'