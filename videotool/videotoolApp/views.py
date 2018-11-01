from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.core.cache import cache
#get serial connection
from libs import serial_connection as serial
from libs import telnet_operation as telnet
import time
#sc = serial.SerialConnection()
debugmode = 1 # if this value is 1, click connect will not use real telnet to link device and master
def showtest(request):
    return render(request,'test.html')

def connection(request):
    if debugmode==0:
        qdmodel = request.POST.get("qdmodel")
        devices = QuantumDevice.objects.all()
        for device in devices:
            if device.qdmodel in qdmodel:
                qddeviceid = device.id
                cache.set('qddeviceid',deviceid)
                break
            else:
                continue
        else:
            print("no this qddevice in qddatabase")
            cache.set('qddeviceid',deviceid)
            return JsonResponse({"comName":None})
        if qdmodel == '780E':
            sc = serial.SerialConnection()
            comName = sc.get_serial_name()
        
        else:    
            comName = "None"
        sc.serial_close()
        return JsonResponse({"comName":comName})
    else:
        cache.set('qddeviceid',1)
        return JsonResponse({"comName":'COM99'})

def qddeviceselect(request):
    qddeviceid = cache.get('qddeviceid')
    
    sut2ports = Quantum2QDoutput.objects.filter(quantum_model = qddeviceid)
    list = []
    for obj in sut2ports:
        port = QDoutport.objects.get(pk=obj.qdport_type)
        list.append(port.qport)
    data = {'qdoutporttype':list}
    return JsonResponse(data,safe=False)
    
        
        
def showdevice(request):
    
    if  debugmode==0:
        ipAddress = request.POST.get("ipaddress")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(ipAddress)
        tn = telnet.TelnetApp(ipAddress,username,password)
        out = tn.excut_command('show device')
        print(out)
        device_number,device_name,ip_device,device_serial= tn.parse_get_device_and_ip(out)
        return JsonResponse({"device_name":device_name,"device_number":device_number})
    else:
        device_number = ['00000', '01301', '01401', '05001', '05008', '05009', '05555', '32001', '32002', '32003']
        device_name = ['(00396)NX-1200 Master', '(00526)CTP-1301', '(00528)VPX-1401', '(00397)NX-1200', '(00530)PR01-0808', '(01383)PR01-RX', '(00530)PR01-0808', '(00526)CTP-1301', '(00262)NSX Application', '(00262)NSX Application']
        
        return JsonResponse({"device_name":device_name,"device_number":device_number})
        

import csv
from .models import Resolution
#add resolution to database;
def addresolution(request):
    path = "d:\ResolutionData.csv"

    with open(path, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            res = Resolution.createResolution(row['res'],
                                              row['expres'],
                                              row['CODE'],
                                              row['EDID'],
                                              row['DTD'],
                                              row['CVT'],
                                              row['RB'],
                                              row['DATE'],
                                              row['DMTID'],
                                              row['STDID'],
                                              row['CVTID'],
                                              row['VIC'],
                                              row['HVIC'],
                                              row['AR'],
                                              row['HTOT'],
                                              row['HRES'],
                                              row['HSPD'],
                                              row['HSPW'],
                                              row['HSPP'],
                                              row['SCAN'],
                                              row['VRAT'],
                                              row['VTOT'],
                                              row['VRES'],
                                              row['VSPD'],
                                              row['VSPW'],
                                              row['VSPP'],
                                              row['PCLK'],
                                              )
            res.save()
    return HttpResponse("add resolutions done")

#from .models import AMX_SUT,Sutport,Sut2Sutinport,Sut2Sutouport,Sutinport2PR0808,Sutoutport2PR0808,PR0808_input,PR0808_output
from .models import *

def querydevicein(request):
    # need optimize with def querydeviceout(request)
    #find input porttype according to device name
    devicename = request.GET.get("devicename")
    devices = AMX_SUT.objects.all()
    for device in devices:
        if device.sModel in devicename:
            deviceid = device.id
            cache.set('deviceid',deviceid)
            break
        else:
            continue
    else:
        print("no this device in database")
        cache.set('deviceid',None)
        return JsonResponse({'porttype':[]},safe=False)
    sut2ports = Sut2Sutinport.objects.filter(ssut = deviceid)
    list = []
    for obj in sut2ports:
        port = Sutport.objects.get(pk=obj.ssutinport)
        list.append(port.sport)
    data = {'porttype':list}
    return JsonResponse(data,safe=False)

def querydeviceout(request):
    #find output porttype according to device name
    #devicename = request.GET.get("devicename")
    # this delay is make sure cache is writed done
    time.sleep(0.5)
    deviceid = cache.get('deviceid')
    print('+++++')
    print(deviceid)
    print('+++++')
    if   deviceid:
        pass
    else:
        print('querydeviceout'+'cache deviceid is not got')
        return JsonResponse({'porttype':[]},safe=False)
    
    sut2ports = Sut2Sutouport.objects.filter(ssut = deviceid)
    list = []
    for obj in sut2ports:
        port = Sutport.objects.get(pk=obj.ssutoutport)
        list.append(port.sport)
    data = {'porttype':list}
    return JsonResponse(data,safe=False)

def queryportin(request):
    portnamein = request.GET.get("portnamein")
    
    
    deviceid = cache.get('deviceid')
    print('xxxxxx')
    print(deviceid)
    print('yyyyy')
    if  deviceid:
        pass
    else:
        print('CACHE IS NOT EXIST NOW!')
        return JsonResponse({'portnumberselect_in':[]},safe=False)
    table_name = AMX_SUT.objects.get(pk=deviceid).sutinport2device
    port = Sutport.objects.get(sport=portnamein)
    print('sdfsdf'+str(port.id))
    strr = table_name+'.objects.filter(sutinport_id=port.id)'
    portobjs = eval(strr)
    #portobjs = Sutinport2PR0808.objects.filter(sutinport_id=port.id)
    list = []
    table_name2 = AMX_SUT.objects.get(pk=deviceid).device_input
    
    for obj in portobjs:
        #var = PR0808_input.objects.get(pk=obj.pr_inportid)
        strr2 = table_name2+'.objects.get(pk=obj.pr_inportid)'
        var  = eval(strr2) 
        list.append(var.portname+"-"+var.inportnumber.__str__())
    data = {'portnumberselect_in':list}
    print (data)
    return JsonResponse(data,safe=False)

def queryportout(request):
    portnameout = request.GET.get("portnameout")
    
    deviceid = cache.get('deviceid')
    print('wwwww')
    print(deviceid)
    print('vvvvvv')
    if   deviceid:
        pass
    else:
        print('queryportout'+'deviceid cache is not got')
        return JsonResponse({'portnumberselect_out':[]},safe=False)
    table_name = AMX_SUT.objects.get(pk=deviceid).sutoutput2device
    port = Sutport.objects.get(sport=portnameout)
    print(port.id)
    strr = table_name+'.objects.filter(sutoutport_id=port.id)'
    portobjs = eval(strr)
    #portobjs = Sutoutport2PR0808.objects.filter(sutoutport_id=port.id)
    list = []
    table_name2 = AMX_SUT.objects.get(pk=deviceid).device_output
    for obj in portobjs:
        #var = PR0808_output.objects.get(pk=obj.pr_outportid)
        strr2 = table_name2+'.objects.get(pk=obj.pr_outportid)'
        var  = eval(strr2) 
        list.append(var.portname+"-"+var.outportnumber.__str__())
    data = {'portnumberselect_out':list}
    print (data)
    return JsonResponse(data,safe=False)
