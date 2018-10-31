from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.

#get serial connection
from libs import serial_connection as serial
from libs import telnet_operation as telnet

#sc = serial.SerialConnection()

def showtest(request):
    return render(request,'test.html')

def connection(request):
    qdmodel = request.POST.get("qdmodel")
    if qdmodel == '780E':
        sc = serial.SerialConnection()
        comName = sc.get_serial_name()
    else:
        comName = "None"
    sc.serial_close()
    return JsonResponse({"comName":comName})

def showdevice(request):
    ipAddress = request.POST.get("ipaddress")
    username = request.POST.get("username")
    password = request.POST.get("password")
    print(ipAddress)
    tn = telnet.TelnetApp(ipAddress,username,password)
    out = tn.excut_command('show device')
    print(out)
    device_number,device_name,ip_device,device_serial= tn.parse_get_device_and_ip(out)
    return JsonResponse({"device_name":device_name})

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
            break
        else:
            continue
    else:
        print("no this device in database")
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
    devicename = request.GET.get("devicename")
    devices = AMX_SUT.objects.all()
    for device in devices:
        if device.sModel in devicename:
            deviceid = device.id
            break
        else:
            continue
    else:
        print("no this device in database")
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
    devicename = request.GET.get("devicename")
    print('xxxxxx')
    print(devicename)
    print('yyyyy')
    devices = AMX_SUT.objects.all()
    for device in devices:
        if device.sModel in devicename:
            deviceid = device.id
            break
        else:
            continue
    else:
        print("no this device in database")
        return JsonResponse({'porttype':[]},safe=False)
    table_name = AMX_SUT.objects.get(pk=deviceid).sutinport2device
    port = Sutport.objects.get(sport=portnamein)
    print(port.id)
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
    devicename = request.GET.get("devicename")
    print('xxxxxx')
    print(devicename)
    print('yyyyy')
    devices = AMX_SUT.objects.all()
    for device in devices:
        if device.sModel in devicename:
            deviceid = device.id
            break
        else:
            continue
    else:
        print("no this device in database")
        return JsonResponse({'porttype':[]},safe=False)
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