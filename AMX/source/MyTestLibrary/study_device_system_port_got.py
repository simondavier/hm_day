# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 17:52:41 2018

@author: WeicZhang
"""

import autoit as ai


ai.win_activate('[title:NetLinx Studio]')


ai.control_list_view('[title:NetLinx Studio]','SysListView322','SelectAll')
haha=ai.control_list_view('[title:NetLinx Studio]','SysListView322','GetSelectedCount')
print (haha ) 

