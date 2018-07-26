
 WinActivate("[title:NetLinx Studio]")
Opt("MouseCoordMode", 2) ;

 MouseClick("left",255,14)
 Sleep(500)

 MouseClick("left",255,25)
 sleep(500)
 WinWaitActive("[title:NetLinx Device Notifications Options]","",5)
 ;ControlClick("[title:NetLinx Device Notifications Options]","","Button1");open notificatioin
 sleep(100)
 ControlClick("[title:NetLinx Device Notifications Options]","","Button5")
 sleep(200)
 ControlClick("[title:NetLinx Device Notifications Options]","","Button2")
 sleep(100)
 WinWaitActive("[title:NetLinx Notification Properties - [Add]]","",5)
 sleep(100)
 ControlSetText("[title:NetLinx Notification Properties - [Add]]","","Edit1","32001")
 ControlSetText("[title:NetLinx Notification Properties - [Add]]","","Edit2","2")
 ControlSetText("[title:NetLinx Notification Properties - [Add]]","","Edit3","1")
 ControlClick("[title:NetLinx Notification Properties - [Add]]","","Button4");clear all first
MouseClick("left",40,252)
MouseClick("left",40,267)
 ControlClick("[title:NetLinx Notification Properties - [Add]]","","Button7");click ok
 sleep(100)
WinActivate("[title:NetLinx Device Notifications Options]")
sleep(500)
 ControlClick("[title:NetLinx Device Notifications Options]","","Button6")

;ControlListView("[title:NetLinx Notification Properties - [Add]]","","SysListView321","Select",2,5)

;~ WinActivate("[title:NetLinx Notification Properties - [Add]]")

;~ Opt("MouseCoordMode", 2) ;

;~ MouseClick("left",40,252)
;~ MouseClick("left",40,267)








;~ MouseClick("left",650,50)
;~ WinWaitActive("[title:Send to NetLinx Device]","",5)
;~ ControlClick("[title:Send to NetLinx Device]","","Button2");explorler the folder name
;~ WinWaitActive("[title:Select Folder]","",5)
;~ ControlSetText("[title:Select Folder]","","Edit1","D:\projects")
;~ sleep(500)
;~ ControlClick("[title:Select Folder]","","Button1")
;~ WinActivate("[title:Send to NetLinx Device]")
;~ MouseClick("left",60,155);click the firmware list item
;~ sleep(500)
;~ ControlClick("[title:Send to NetLinx Device]","","Button7")
