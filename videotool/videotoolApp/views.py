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
        cache.set('qddeviceid',2)
        return JsonResponse({"comName":'COM99'})

def qddeviceselect(request):
    qddeviceid = cache.get('qddeviceid')
    
    sut2ports = Quantum2QDoutput.objects.filter(quantum_model = qddeviceid)
    list = []#output signal list
    for obj in sut2ports:
        port = QDoutport.objects.get(pk=obj.qdport_type)
        list.append(port.qport)
    #data = {'qdoutporttype':list}
    pts = QuantumInConnecter.objects.all()
    
    list2 = []#input connector list
    for obj in pts:
        
        list2.append(obj.qdinconnector)
    print(list2) 
    pts3 = QuantumOutConnecter.objects.all()
    list3 = []#output connector list
    
    for obj in pts3:
        
        list3.append(obj.qdoutconnector)
    print(list3)     
    data = {'qdoutporttype':list,'qdinporttype':list2,'qdoutconnector':list3}
    return JsonResponse(data,safe=False)
def mapping_method(deviceid):
    pass
    
def qdpattern(request):
    
    pts = Qdpattern.objects.all()
    list = []
    list2 = []
    for obj in pts:
        
        list.append(obj.qpattern)
        list2.append(obj.id)
    data = {'qdpatterns':list,'pk':list2}
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
    returnedname = devicename.split('---')[0]
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
        return JsonResponse({'porttype':[],'returnedname':None},safe=False)
    sut2ports = Sut2Sutinport.objects.filter(ssut = deviceid)
    list = []
    for obj in sut2ports:
        port = Sutport.objects.get(pk=obj.ssutinport)
        list.append(port.sport)
    data = {'porttype':list,'returnedname':returnedname}
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
def querytimingin(request):
    portnamein = request.GET.get("portnamein")
    portnumberin = request.GET.get("portnumberin")
    print('querytimgingin')
    print(portnamein)
    print(portnumberin)
    print('querytimgingin')
    
    deviceid = cache.get('deviceid')
    
    if  deviceid:
        pass
    else:
        print('CACHE IS NOT EXIST NOW!')
        return JsonResponse({'timingselect_in':[],'timingselect_in_id':[]},safe=False)
    status = request.GET.get('QDOUTPUTFILTER')
    if status=='Available':
        table_name = AMX_SUT.objects.get(pk=deviceid).sutinport2device
        
        port = Sutport.objects.get(sport=portnamein)
        print('sdfsdf'+str(port.id))
        strr = table_name+'.objects.filter(sutinport_id=port.id)'
        portobjs = eval(strr)
        #portobjs = Sutinport2PR0808.objects.filter(sutinport_id=port.id)
        list = []
        list2= []
        table_name2 = AMX_SUT.objects.get(pk=deviceid).device_input
        table_name3 = AMX_SUT.objects.get(pk=deviceid).timing2deviceinput#for port&timging mapping table
        
        for obj in portobjs:
            #var = PR0808_input.objects.get(pk=obj.pr_inportid)
            strr2 = table_name2+'.objects.get(pk=obj.pr_inportid)'
            var  = eval(strr2) 
            if portnumberin==(var.portname+"-"+var.inportnumber.__str__()):
                strr3 = table_name3+'.objects.filter(pr_inport=obj.pr_inportid)'
                resolutions  = eval(strr3) 
                for objj in resolutions:
                    options = Resolution.resObject.get(pk=objj.res)
                    list.append(options.res)
                    list2.append(options.id)
        data = {'timingselect_in':list,'timingselect_in_id':list2}
        #print (data)
        return JsonResponse(data,safe=False)
    else:
        list=[]
        list2=[]
        resolutions = Resolution.resObject.all()
        for resolution in resolutions:
            list.append(resolution.res)
            list2.append(resolution.id)
        data = {'timingselect_in':list,'timingselect_in_id':list2}
        return JsonResponse(data,safe=False)
def querytimingout(request):
    portnameout = request.GET.get("portnameout")
    portnumberout = request.GET.get("portnumberout")
    print('querytimgingout')
    print(portnameout)
    print(portnumberout)
    print('querytimgingout')
    
    deviceid = cache.get('deviceid')
    
    if  deviceid:
        pass
    else:
        print('CACHE IS NOT EXIST NOW!')
        return JsonResponse({'timingselect_out':[],'timingselect_out_id':[]},safe=False)
    status = request.GET.get('QDOUTPUTFILTER')
    if status=='Available':
        table_name = AMX_SUT.objects.get(pk=deviceid).sutoutput2device
        
        port = Sutport.objects.get(sport=portnameout)
        print('sdfsdf'+str(port.id))
        strr = table_name+'.objects.filter(sutoutport_id=port.id)'
        portobjs = eval(strr)
        #portobjs = Sutinport2PR0808.objects.filter(sutoutport_id=port.id)
        list = []
        list2 = []
        table_name2 = AMX_SUT.objects.get(pk=deviceid).device_output
        table_name3 = AMX_SUT.objects.get(pk=deviceid).timing2deviceoutput#for port&timging mapping table
        
        for obj in portobjs:
            #var = PR0808_input.objects.get(pk=obj.pr_outportid)
            strr2 = table_name2+'.objects.get(pk=obj.pr_outportid)'
            var  = eval(strr2) 
            if portnumberout==(var.portname+"-"+var.outportnumber.__str__()):
                strr3 = table_name3+'.objects.filter(pr_outport=obj.pr_outportid)'
                resolutions  = eval(strr3) 
                for objj in resolutions:
                    options = Resolution.resObject.get(pk=objj.res)
                    list.append(options.res)
                    list2.append(options.id)
        data = {'timingselect_out':list,'timingselect_out_id':list2}
        #print (data)
        return JsonResponse(data,safe=False)
    else:
        list=[]
        list2=[]
        resolutions = Resolution.resObject.all()
        for resolution in resolutions:
            list.append(resolution.res)
            list2.append(resolution.id)
        data = {'timingselect_out':list,'timingselect_out_id':list2}
        return JsonResponse(data,safe=False)
def receive_submit(request):
    # {'ip':ip,'username':username,'passwordd':passwordd,'porttypeselect_in':porttypeselect_in,'portnumberselect_in':portnumberselect_in,
        # 'timingselect_in':timingselect_in,'porttypeselect_out':porttypeselect_out,'portnumberselect_out':portnumberselect_out,'timingselect_out':timingselect_out,
        # 'QDOUTPUTSIGNAL':QDOUTPUTSIGNAL,'QDOUTPUTCONNECTOR':QDOUTPUTCONNECTOR,'QDINPUTSIGNAL':QDINPUTSIGNAL,'devicenumber':devicenumber,'portt':portt,'system':system}
    deviceid = cache.get('deviceid')
    cache.set('ip',request.GET.get("ip"))
    cache.set('username',request.GET.get("username"))
    cache.set('passwordd',request.GET.get("passwordd"))
    print(request.GET.get("timingselect_in"))
    try:
        cache.set('porttypeselect_in',Sutport.objects.get(sport=request.GET.get("porttypeselect_in")).id)
    except:
        cache.set('porttypeselect_in',None)
    print(cache.get('porttypeselect_in'))
    cache.set('portnumberselect_in',request.GET.get("portnumberselect_in"))
    cache.set('timingselect_in',request.GET.get("timingselect_in"))
   
    print(request.GET.get("timingselect_in"))
    try:
        cache.set('porttypeselect_out',Sutport.objects.get(sport=request.GET.get("porttypeselect_out")).id)
    except:
        cache.set('porttypeselect_out',None)
    print(cache.get('porttypeselect_out'))
    cache.set('portnumberselect_out',request.GET.get("portnumberselect_out"))
    cache.set('timingselect_out',request.GET.get("timingselect_out"))
    print(cache.get('timingselect_out'))
    cache.set('QDOUTPUTSIGNAL',QDoutport.objects.get(qport=request.GET.get("QDOUTPUTSIGNAL")).id)#table is QDoutport
    cache.set('QDINPUTSIGNAL',QuantumInConnecter.objects.get(qdinconnector=request.GET.get("QDINPUTSIGNAL")).id)#table is QuantumInConnecter
    cache.set('QDOUTPUTCONNECTOR',QuantumOutConnecter.objects.get(qdoutconnector=request.GET.get("QDOUTPUTCONNECTOR")).id)#table is  QuantumOutConnecter
    #cache.set('QDOUTPUTSIGNAL',request.GET.get("QDOUTPUTSIGNAL"))
    #cache.set('QDOUTPUTCONNECTOR',request.GET.get("QDOUTPUTCONNECTOR"))
    #cache.set('QDINPUTSIGNAL',request.GET.get("QDINPUTSIGNAL"))
    cache.set('devicenumber',request.GET.get("devicenumber"))
    cache.set('portt',request.GET.get("portt"))
    cache.set('system',request.GET.get("system"))
    cache.set('colorrange',request.GET.get("colorrange"))
    cache.set('samplingmode',request.GET.get("samplingmode"))
    cache.set('saclertype',request.GET.get("saclertype"))
    cache.set('TX_Video_Timing',request.GET.get("TX_Video_Timing"))
    cache.set('RX_Video_Timing',request.GET.get("RX_Video_Timing"))
    print(cache.get('RX_Video_Timing'))# return value is on or off
    cache.set('QDOUTPUTFILTER',request.GET.get("QDOUTPUTFILTER"))
    
    #username = request.GET.get("username")
    
    return JsonResponse(None,safe=False)




    