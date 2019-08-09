#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import re
import quantum780_operation as qdoperation
import switchconfig_operation as switchconfig
import telnet_operation as telnet
import logger as log
import terminalcolor as tcolor
from optparse import OptionParser
#log.disable(log.logger.info) #disable log

SWITCHCONFIG = "ConfigResolutionData.xlsx"
INPCOUNT = 0 #count the pass number
OUTPCOUNT = 0 #count the pass number
INFCOUNT = 0 #count the fail number
OUTFCOUNT = 0 #count the fail number
logname = ".\\log\\" + time.strftime("%Y%m%d_%H%M%S") + ".log"
log = log.Logger(logname)

def execute_test(cmdoptions, cmdargs):
    """
    Execute the test;
    :param cmdoptions:
    :param cmdargs:
    :return:
    """
    global INPCOUNT, OUTPCOUNT,INFCOUNT,OUTFCOUNT, TESTPARAS, outport, outporttype
    print("Your Test will be start after 3 seconds, please wait...")
    loadProcess()
    #Get config from the data sheet:
    config_d = switchconfig.SwitchConfigOperation(SWITCHCONFIG, 1).load_config()
    log.logger.info(config_d)
    filename = config_d['ConfigFilePath']
    edidfile = config_d['EdidFilePath']
    log.logger.info(cmdoptions)
    tn = telnet.TelnetApp(config_d['MasterIP'],config_d['MasterUsername'],config_d['MasterPassword'])
    log.logger.info("switch_ip:"+config_d['SwitchIP']+"switch_username:"+config_d['SwitchUsername']+"Switch_pwd:" \
              +config_d['SwitchPassword'])
    swcregconf = switchconfig.SwitchConfigOperation(filename, 0)
    swcolorconfig = switchconfig.SwitchConfigOperation(filename, 2)
    qd = qdoperation.Quantum780Operation()
    inportdic = initPort(config_d['InputPortType'])
    log.logger.info("The input port type is:%s."% inportdic)
    outportdic = initPort(config_d['OutputPortType'])
    log.logger.info("The output port type is:%s."% outportdic)
    # initialize the port;
    outport = config_d['SutDPS'].split(":")[1]
    #Test Step:
    #Ignore HDMI proctocal test parametres;
    if cmdoptions.ignore != "None":
        qd.TESTPARAS.remove(cmdoptions.ignore)
        swcregconf.TESTPARAS.remove(cmdoptions.ignore)
    #Initialize QD generator, default:1080p
    log.logger.info("Start initialize Quantum Data!")
    qd.sent_qd_generator('1080p60', cmdoptions.patternname, \
                         cmdoptions.colorspace, \
                         cmdoptions.deepcolor, \
                         cmdoptions.outport, \
                         cmdoptions.hdcp)
    #Initialize SUT default input and output
    log.logger.info("Start initialize DUT in/out port!")
    inport = inportdic['HDMI1']
    inporttype = 'HDMI1'
    outport = outportdic['HDMI1']
    outporttype = 'HDMI1'
    cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outportdic['HDMI1'])
    # Set Switch output
    switchport = "".join(re.findall(r"\d", outporttype))
    cmd_sw = ''.join('ci' + switchport + 'oall')
    tn.send_thor_cmd(config_d['SutDPS'], cmd_dut)
    tn.send_thor_cmd(config_d['SwitchDPS'], cmd_sw)
    log.logger.info("Hey,Testing Start......")
    repetitions = int(cmdoptions.repetitions)
    ar = cmdoptions.aspectratio
    incolor = cmdoptions.colorspace
    outcolor = cmdoptions.outcolorspace
    aspectratio = cmdoptions.aspectratio

    # Execute repetions
    while(repetitions):
        for qdcode in getTimingList(swcregconf, cmdoptions.timing, 37):
            log.logger.info("The current input timing is %s" % qdcode)
            # Get the input code to get h,v
            incode= swcregconf.getTimingExpect(qdcode)
            #Set input timing
            qd.sent_qd_generator(qdcode)
            #If input skip protocal test
            if 'protocal' == cmdoptions.skip:
                pass
            else:
                #Check the input timing only
                if checkTiming(qd, qdcode, swcregconf, 'input'):
                    INPCOUNT = INPCOUNT+1
                else:INFCOUNT = INFCOUNT+1

            #Set Dut switch paraeters, paser "--random";
            if cmdoptions.random != None:
                time.sleep(int(cmdoptions.interval))
                cmd_dut,cmd_sw, outport, outporttype, inporttype = randSwitchPort(cmdoptions.random, inportdic, outportdic)
                log.logger.info("The input port is %s" % inporttype)
                log.logger.info("The output port is %s" % outporttype)
                #Check if input port support HDBT Big 4K
                if isHdbtSupport(cmdoptions, qdcode, inporttype):
                    pass
                else:
                    continue
                #input support
                log.logger.info("Switch the DUT port is: %s" % cmd_dut)
                tn.send_thor_cmd(config_d['SutDPS'], cmd_dut)
                log.logger.info("Switch the Switch port is: %s" % cmd_sw)
                tn.send_thor_cmd(config_d['SwitchDPS'], cmd_sw)
            #If bypass, Yes:dectected；Not:set output timing
            if 'bypass' == cmdoptions.scaletiming:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                #Set DUT output: bypass；Set port to output
                if cmdoptions.random != 'None':
                    newdps = config_d['SutDPS'].replace(":1:",":"+outport+":")
                    log.logger.info("The new SUT DPS is %s" % newdps)
                    tn.send_thor_cmd(newdps,'VIDOUT_SCALE-BYPASS')
                else:tn.send_thor_cmd(config_d['SutDPS'], 'VIDOUT_SCALE-BYPASS')
                #Set QD input port
                log.logger.info("Set QD analyze port!")
                setQdInputport(qd, outporttype)
                # HDBT can not support 4096x2160@50/60 YCbCr/RGB input or output
                if isHdbtSupport(cmdoptions, qdcode, outporttype):
                    pass
                else:
                    continue
                #If output skip protocal/pattern test
                if 'protocal' == cmdoptions.skip:
                    #check bypass pattern
                    pixelcount = qd.query_pixelErrCount(100)
                    if pixelcount:
                        print("Bypass no pixel error, pass")
                    else:
                        print("Bypass has %s pixel error!" % pixelcount)
                elif 'pattern' == cmdoptions.skip:
                    #Check the output
                    if checkTiming(qd, qdcode, swcregconf, 'output'):
                        OUTPCOUNT = OUTPCOUNT+1
                    else:OUTFCOUNT = OUTFCOUNT+1
                else:
                    #Check the output
                    if checkTiming(qd, qdcode, swcregconf, 'output'):
                        OUTPCOUNT = OUTPCOUNT+1
                    else:OUTFCOUNT = OUTFCOUNT+1
                    #check bypass pattern
                    pixelcount = qd.query_pixelErrCount(100)
                    if pixelcount:
                        print("Bypass no pixel error, pass")
                    else:
                        print("Bypass has %s pixel error!" % pixelcount)
            elif 'auto'== cmdoptions.scaletiming: #or 'random'==cmdoptions.scaletiming:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                for scalercode in getTimingList(swcregconf, cmdoptions.scaletiming, 38):
                    #HDBT can not support 4096x2160@50/60 YCbCr/RGB input or output
                    if isHdbtSupport(cmdoptions, scalercode, outporttype):
                        pass
                    else:
                        continue

                    log.logger.info("Set Scaler Out timing to %s!" % scalercode)
                    # set scaler to auto
                    if cmdoptions.random != 'None':
                        newdps = config_d['SutDPS'].replace(":1:", ":" + outport + ":")
                        log.logger.info("The new SUT DPS is %s" % newdps)
                        tn.send_thor_cmd(newdps, 'vidout_scale-auto')
                    else:
                        newdps = config_d['SutDPS']
                        tn.send_thor_cmd(newdps, 'vidout_scale-auto')
                    #"for"  set aspect Ratio
                    arcmd='vidout_aspect_ratio-'+ar
                    tn.send_thor_cmd(newdps, arcmd)
                    log.logger.info("Set aspectratio to %s !" % ar)
                    #set output colorspace
                    cscmd = 'vidout_color_space-'+outcolor
                    tn.send_thor_cmd(newdps, cscmd)
                    log.logger.info("Set output colorspace to %s !" % outcolor)
                    #get the output timing code to get h,v;
                    outcode = swcregconf.getTimingExpect(scalercode)
                    # set qd input port
                    log.logger.info("Set QD analyze port!")
                    setQdInputport(qd, outporttype)
                    # write edid
                    writeEdid(swcregconf, scalercode, edidfile, qd)
                    # if output skip protocal test
                    if 'protocal' == cmdoptions.skip:
                        # check pattern
                        #checkPattern(qd, incode, outcode, swcregconf, ar, colorspace, swcolorconfig)
                        checkPattern(qd, qdcode, scalercode, incode, outcode, aspectratio, incolor, outcolor, swcolorconfig,
                                     colorimetry='auto')
                    elif 'pattern' == cmdoptions.skip:
                        # check output paras
                        if checkTiming(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                    else:
                        # check output paras
                        if checkTiming(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                        # check pattern
                        #checkPattern(qd, incode, outcode, swcregconf, ar, colorspace, swcolorconfig)
                        checkPattern(qd, qdcode, scalercode, incode, outcode, aspectratio, incolor, outcolor, swcolorconfig,
                                     colorimetry='auto')

            else:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                #scalercode = cmdoptions.scaletiming
                for scalercode in getTimingList(swcregconf, cmdoptions.scaletiming, 38):
                    # HDBT can not support 4096x2160@50/60 YCbCr/RGB input or output
                    if isHdbtSupport(cmdoptions, scalercode, outporttype):
                        pass
                    else:
                        continue
                    log.logger.info("Set Scaler Out timing to %s!" % scalercode)
                    # set scaler to manual
                    if cmdoptions.random != 'None':
                        #config_d['SutDPS'] = config_d['SutDPS'].replace(":1:", ":" + outport + ":") need know why not?
                        newdps = config_d['SutDPS'].replace(":1:", ":" + outport + ":")
                        log.logger.info("The new SUT DPS is %s" % newdps)
                        #tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-manual')
                        tn.send_thor_cmd(newdps, 'vidout_scale-manual')
                    else:
                        newdps = config_d['SutDPS']
                        tn.send_thor_cmd(newdps, 'vidout_scale-manual')
                    #"for"  set aspect Ratio
                    arcmd='vidout_aspect_ratio-'+ar
                    tn.send_thor_cmd(newdps, arcmd)
                    log.logger.info("Set aspectratio to %s !" % ar)
                    #set output colorspac
                    cscmd = 'vidout_color_space-'+outcolor
                    tn.send_thor_cmd(newdps, cscmd)
                    log.logger.info("Set output colorspace to %s !" % outcolor)
                    # set scaler output timing
                    outcode = swcregconf.getTimingExpect(scalercode)
                    #write edid to sink
                    #writeEdid(swcregconf, scalercode, edidfile, qd)
                    #VIDOUT_RES_REF
                    cmd=''.join('VIDOUT_RES_REF-'+outcode['HRES']+'x'+outcode['VRES']+','+str(round(float(outcode['VRAT']))))
                    log.logger.info("The manual scaler timing out is %s" % cmd)
                    tn.send_thor_cmd(newdps, cmd)
                    #Set QD input port
                    log.logger.info("Set QD analyze port!")
                    setQdInputport(qd, outporttype)
                    # if output skip protocal test
                    if 'protocal' == cmdoptions.skip:
                        # check pattern
                        #checkPattern(qd, incode, outcode, swcregconf, ar, colorspace, swcolorconfig)
                        checkPattern(qd, qdcode, scalercode, incode, outcode, aspectratio, incolor, outcolor, swcolorconfig,
                                     colorimetry='auto')
                    elif 'pattern' == cmdoptions.skip:
                        # check output paras
                        if checkTiming(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                    else:
                        # check output paras
                        if checkTiming(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                        # check pattern
                            #checkPattern(qd, incode, outcode, swcregconf, ar, colorspace, swcolorconfig)
                        checkPattern(qd, qdcode, scalercode, incode, outcode, aspectratio, incolor, outcolor, swcolorconfig,
                                     colorimetry='auto')
        repetitions = repetitions-1
    #Calculate all test result
    log.logger.info("OK,All Test Completed! Total: "+str(INPCOUNT+INFCOUNT+OUTPCOUNT+OUTFCOUNT)+" cases, "\
                    +str(INPCOUNT+OUTPCOUNT)+" was PASS, " +str(INFCOUNT+OUTFCOUNT)+" was FAIL!")
    log.logger.info("INPUT RESULT:"+str(INPCOUNT)+" is PASS, "+str(INFCOUNT)+" is FAIL. "\
                    "OUTPUT RESULT:"+str(OUTPCOUNT)+" is PASS, "+str(OUTFCOUNT)+" is FAIL")

def initPort(porttype):
    """
    Initalize the DUT port
    :param porttype:
    :return: a port dic
    """
    dic = {}
    portlist = porttype.split(',')
    for opt in portlist:
        dic[opt.split(':')[0]] = opt.split(':')[1]
    return dic

def isHdbtSupport(cmdoptions, qdcode, porttype):
    if 'HDBT' in porttype:
        if qdcode == '2160p50w' or qdcode == '2160p60w':
            if cmdoptions.colorspace == 'RGB' or cmdoptions.colorspace == 'YCbCr444':
                log.logger.info("HDBT "+porttype+" can not support 4096x2160@50/60,RGB/YCbCr444!!!")
                return False
    return True

def setQdInputport(qd, outporttype):
    """
    Set Quantum input analyzer port
    :param qd:
    :param outporttype:
    :return:
    """
    if 'HDMI' in outporttype:
        qd.set_input_signal(0)
    elif 'HDBT' in outporttype:
        qd.set_input_signal(1)
    else:raise("Quantum only support HDMI/HDBT this port type, please check your config file")

def getTimingList(swconfig, timingmode, col):
    if 'all' == timingmode or 'auto' == timingmode or 'manual' == timingmode:
        return swconfig.getSupportTimingCode(col)
    elif 'random' == timingmode:
        return random.choice(swconfig.getSupportTimingCode(col)).split()
    else:
        return timingmode.split()

def checkTiming(qd, qdcode, swcregconf, inout):
    """
    Check the input timing
    :param qd:
    :param qdcode:
    :param swcregconf:
    :param inout:
    :return: boolean
    """
    # get expceted paras
    expect_ioput = swcregconf.getTimingExpect(qdcode)
    time.sleep(8) # Add debug time to delay analyze.
    if('input'==inout):
        if '480i' in qdcode or '576i' in qdcode: #This is a 780E bug in interlace mode.
            expect_ioput['HTOT'] = str(int(expect_ioput['HTOT'])//2)
            expect_ioput['HSPD'] = str(int(expect_ioput['HSPD'])//2)
            expect_ioput['HSPW'] = str(int(expect_ioput['HSPW'])//2)
            expect_ioput['VTOT'] = str(int(expect_ioput['VTOT'])*2)
        #log.logger.info("Get Expected Timing Result!")
        detect_input = qd.generator_timing_dump()
        log.logger.info("=The %s Expected Para are:=" % inout)
        log.logger.info(expect_ioput)
        print("==Input Timing is: " + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput[
            'VRAT'] + "==")
        print("===================================")
        result = swcregconf.compare_result(expect_ioput, detect_input)
        print("Input Timing" + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput['VRAT'] + " test is %s" \
              % result)
        log.logger.info(
            "Input Timing" + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput['VRAT'] + " test is %s" \
            % result)
        # if 'PASS'==result:
        #     return True
        # else: return False
    elif('output'==inout):
        #expect_output = swcregconf.getTimingExpect(qdcode)
        detect_output = qd.alyz_timing_dump()
        log.logger.info("=The %s Expected Para are:=" % inout)
        log.logger.info(expect_ioput)
        print("==Output Timing is: " + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput[
            'VRAT'] + "==")
        print("=====================================")
        result = swcregconf.compare_result(expect_ioput, detect_output)
        print("Output Timing" + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput['VRAT'] + " test is %s" \
              % result)
        log.logger.info(
            "Output Timing" + expect_ioput['HRES'] + "x" + expect_ioput['VRES'] + "@" + expect_ioput['VRAT'] + " test is %s" \
            % result)
    else:raise ("Wrong I/O, function only support 'input' or 'output', please check! ")
    if 'PASS' == result:
        return True
    else:return False

def checkPattern(qd, qdincode, qdoutcode, incode, outcode, aspectratio, incolor, outcolor, swcolorconfig, colorimetry='auto'):
    """

    :param qd: Quantum obj
    :param incode: input paras dic
    :param outcode: output paras dic
    :param ar: AspectRatio, maintain, stretch
    :param colorspace: RGB/YCbCr444/YCbCr422/YCbCr420
    :param swColorConfig: get colorspace expect paras
    :param colorimetry: set colorimetry under YCbCr mode(Auto BT601, BT709, BT2020)
    :return: Boolean
    """
    expect_input = incode
    expect_output = outcode
    if 'stretch' == aspectratio:
        #check outcode
        h= int(expect_output['HRES']) #output hres
        v= int(expect_output['VRES']) #output vres
        #if 4K, 4K capture was not support by 780E
        if '2160p50' in qdincode or '2160p60' in qdincode:
            if '2160p50' in qdoutcode or '2160p60' in qdoutcode:
                log.logger.info("Both In/Out are 4K")
                desarea = calculateBox(1, 1, qd, h, v, h, v, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is: %s" %desarea)
                if compareArea(1, h, v, desarea):
                    return True
                else:return False
            else:
                log.logger.info("In is 4K, Out not 4K")
                desarea = calculateBox(1, 0, qd, h, v, h,v, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(0, h, v, desarea):
                    tcolor.cprint('Pattern Test was Pass','GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
        else:
            if '2160p50' in qdoutcode or '2160p60' in qdoutcode:
                log.logger.info("In not 4K, Out is 4K")
                desarea = calculateBox(0, 1, qd, h, v, h ,v, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(1, h, v, desarea):
                    tcolor.cprint('Pattern Test was Pass', 'GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
            else:
                log.logger.info("Both are not 4K")
                desarea = calculateBox(0, 0, qd, h, v, h, v, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(0, h, v, desarea):
                    tcolor.cprint('Pattern Test was Pass', 'GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
    elif 'maintain' == aspectratio:
        print("in maintain")
        #Get scale fators
        h1 = int(expect_input['HRES'])
        v1 = int(expect_input['VRES'])
        h2 = int(expect_output['HRES'])
        v2 = int(expect_output['VRES'])
        print(h1)
        print(v1)
        print(h2)
        print(v2)
        hsf = float("%.3f" % float(h2/h1))
        print(hsf)
        vsf = float("%.3f" % float(v2/v1))
        print(vsf)
        sf = min(hsf, vsf)
        print(sf)
        h3 = round(sf*h1)
        print("The Horizontal line is %d" % h3)
        v3 = round(sf*v1)
        print("The Vertical line is %d" % v3)
        if '2160p50' in qdincode or '2160p60' in qdincode:
            if '2160p50' in qdoutcode or '2160p60' in qdoutcode:
                log.logger.info("Both In/Out are 4K")
                desarea = calculateBox(1, 1, qd, h2, v2, h3, v3, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is: %s" %desarea)
                if compareArea(1, h3, v3, desarea):
                    return True
                else:return False
            else:
                log.logger.info("In is 4K, Out not 4K")
                desarea = calculateBox(1, 0, qd, h2, v2, h3, v3, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(0, h3, v3, desarea):
                    tcolor.cprint('Pattern Test was Pass','GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
        else:
            if '2160p50' in qdoutcode or '2160p60' in qdoutcode:
                log.logger.info("In not 4K, Out is 4K")
                desarea = calculateBox(0, 1, qd, h2, v2, h3, v3, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(1, h3, v3, desarea):
                    tcolor.cprint('Pattern Test was Pass', 'GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
            else:
                log.logger.info("Both are not 4K")
                desarea = calculateBox(0, 0, qd, h2, v2, h3, v3, incolor, outcolor, swcolorconfig)
                log.logger.info("The dest area is:")
                log.logger.info(desarea)
                if compareArea(0, h3, v3, desarea):
                    tcolor.cprint('Pattern Test was Pass', 'GREEN')
                    return True
                else:
                    tcolor.cprint('Pattern Test was Fail', 'RED')
                    return False
    else:
        raise ("Unsupport aspectration was set.")

def compareArea(outflag, h, v, desarea):
    """
    Copare black box area;
    :param h: src width
    :param v: src hight
    :return:boolean
    """
    x = h
    y = v
    # this "if" according to 780E can not support 4K capture
    if outflag:
        x = round(x/2)
        y = round(y/2)
    srcarea = round((y*x)/4)
    log.logger.info("The destiny is:%s" % str(desarea))
    log.logger.info("The source  is:%s" % str(srcarea))
    factor = ("%.2f" % float(srcarea/desarea))
    log.logger.info("The factor is :"+ factor)
    #compare black box
    if factor == "1.01" or factor == "1.00" or factor == "0.99":
        return True
    else:
        return False


def getExpectColor(swcolorconfig, inflag, outflag, incolor, outcolor):
    """
    Get expect color
    :param swcolorconfig:
    :param inflag: if 4k, 4k=1, non4k=0
    :param outflag: if 4k, 4k=1, non4k=0
    :param incolor:
    :param outcolor:
    :return: white color
    """
    return swcolorconfig.getExpectPixelColor(inflag,outflag,incolor,outcolor)

def compColor(expcolor, pcolor):
    """
    Compare 2 Hex str color
    :param expcolor:
    :param pcolor:
    :return: boolean
    """
    expcolor = re.findall(r"0x\w+", expcolor)
    pcolor = re.findall(r"0x\w+", pcolor)
    for i in range(len(pcolor)):
        pcolor[i]=int(pcolor[i],16)
        expcolor[i]=int(expcolor[i],16)
    for i in range(len(pcolor)):
        if abs(pcolor[i]-expcolor[i])<=2:
            return True
        else:return False

def calculateBox(inflag, outflag, qd, h1, v1, h2, v2, incolor, outcolor, swcolorconfig):
    """
    Calculate black/white points of the pattern.
    :param inflag: if 4K, flag =1;
    :param outflag: if 4K, flag =1;
    :param qd;
    :param h1;
    :param v1;
    :param h2;
    :param v2;
    :param incolor;
    :param outcolor;
    :param swcolorconfig;
    :return: black box area;
    """
    x = h1
    y = v1
    width = h2
    hight = v2
    offset = 20 #pixel detect offset
    # this "if" according to 780E can not support 4K capture
    if outflag:
        x = round(x/2)
        y = round(y/2)
        width = round(width/2)
        hight = round(hight/2)
    #get the expect color
    expcolor = getExpectColor(swcolorconfig, inflag, outflag, incolor, outcolor)
    #init pixel analyzer
    qd.init_capture()
    qd.cap_frame(100)
    qd.init_compare_frame()
    qd.query_pixelErrCount(100)
    #get the ynorth
    xcenter = round(x/2)
    ycenter=round(y/2)-round(hight/4)+offset/2
    limit = ycenter-offset
    log.logger.info("finding ynorth...")
    while ycenter > limit:
        pcolor = qd.get_pixel(str(xcenter), str(ycenter))
        if compColor(expcolor, pcolor):
            ynorth = ycenter
            break
        ycenter=ycenter-1
    else:
        ynorth = 0
        log.logger.info("ynorth can not find!")
    log.logger.info("ynorth is %s" % ynorth)
    #get the ysouth
    xcenter = round(x/2)
    #ycenter=round((y/4)*3-10)
    ycenter=round(y/2)+round(hight/4)-offset/2
    limit = ycenter+offset
    log.logger.info("finding ysouth...")
    while ycenter < limit: #10 pixel offset
        pcolor = qd.get_pixel(str(xcenter), str(ycenter))
        if compColor(expcolor, pcolor):
            ysouth = ycenter
            break
        ycenter=ycenter+1
    else:
        ysouth = y
        log.logger.info("ysouth can not find!")
    log.logger.info("ysouth is %s" % ysouth)
    #get the xwest
    #xcenter=round((x/4)+10)
    xcenter=round(x/2)-round(width/4)+offset/2
    ycenter = round(y/2)
    limit = xcenter-offset
    log.logger.info("finding xwest...")
    while xcenter > limit:
        pcolor = qd.get_pixel(str(xcenter), str(ycenter))
        if compColor(expcolor, pcolor):
            xwest = xcenter
            break
        xcenter=xcenter-1
    else:
        xwest = 0
        log.logger.info("xwest can not find!")
    log.logger.info("xwest is %s" % xwest)
    #get the xeast
    #xcenter=round((x/4)*3-10)
    xcenter=round(x/2)+round(width/4)-offset/2
    ycenter = round(y/2)
    limit = xcenter+offset
    log.logger.info("finding xeast...")
    while xcenter < limit:
        pcolor = qd.get_pixel(str(xcenter), str(ycenter))
        if compColor(expcolor, pcolor):
            xeast = xcenter
            break
        xcenter=xcenter+1
    else:
        xeast = x
        log.logger.info("xeast can not find!")
    log.logger.info("xeast is %s" % xeast)
    hight = ysouth - ynorth
    width = xeast - xwest
    return hight*width

def randSwitchPort(rand, inportdic, outportdic):
    """
    random switch the DUT and Switcher
    :param random:
    :param inportdic:
    :param outportdic:
    :return:
    """
    if 'all' == rand:
        #Random switch SUT in port
        inporttype = random.choice(list(inportdic.keys()))
        inport = inportdic[inporttype]
        #Random switch SUT out port
        outporttype = random.choice(list(outportdic.keys()))
        outport = outportdic[outporttype]
        cmd_dut = ''.join('ci' + inport + 'o' + outport)
        log.logger.info("Set the DUT port is: %s" % cmd_dut)
        #Set Switch output
        switchport = "".join(re.findall(r"\d",outporttype))
        cmd_sw = ''.join('ci'+switchport+'oall')
        #log.logger.info("Set the Switch port is: %s" % cmd_sw)
    elif 'input' == rand:
        # Random switch SUT in port, output default is first port
        inporttype = random.choice(list(inportdic.keys()))
        inport = inportdic[inporttype]
        cmd_dut = ''.join('ci' + inport + 'o' + outportdic['HDMI1'])
        log.logger.info("The DUT IN port is: %s" % inport)
        #No output switch
        log.logger.info("OUTput has no change.")
        # Set Switch output
        cmd_sw = ''
    elif 'output' == rand:
        #No switch SUT in port, input is the default
        log.logger.info("INput has no change.")
        outporttype = random.choice(list(outportdic.keys()))
        outport = outportdic[outporttype]
        cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outport)
        log.logger.info("The DUT OUT port is: %s" % outport)
        #Set Switch output
        switchport = "".join(re.findall(r"\d",outporttype))
        cmd_sw = ''.join('ci'+switchport+'oall')
        #log.logger.info("Set the Switch port is: %s" % cmd_sw)
    else:
        cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outportdic['HDMI1'])
        #Set Switch output
        switchport = "".join(re.findall(r"\d",'HDMI1'))
        cmd_sw = ''.join('ci'+switchport+'oall')
    return cmd_dut, cmd_sw, outport, outporttype, inporttype

def writeEdid(swcregconf, scalercode, edidfile, qd):
    edid = swcregconf.qdcode2edid(scalercode)
    log.logger.info("The new edid is:" + edid)
    edidobj = switchconfig.SwitchConfigOperation(edidfile, 0)
    block0 = edidobj.getEdid(edid, '0')
    block1 = edidobj.getEdid(edid, '1')
    # 4.2 write edid:
    qd.write_edid_block('0', str(block0))
    qd.write_edid_block('1', str(block1))
    # 4.3 apply edid
    qd.apply_edid()

def loadProcess():
    lineLength = 100
    delaySeconds = 0.03
    frontSymbol = '='
    frontSymbol2 = ['-', '\\', '|', '/']
    backSymbol = ' '
    lineTmpla = "{:%s<%s} {} {:<2}" % (backSymbol, lineLength)
    for j in range(lineLength):
        tmpSymbol = frontSymbol2[j % (len(frontSymbol2))]
        print("\r" + lineTmpla.format(frontSymbol * j, tmpSymbol, j), end='')
        time.sleep(delaySeconds)
    print("")

def main():
    """
    :return:
    """
    usage = "usage: %prog [options] args"
    parser = OptionParser(usage)
    parser.add_option("-p", dest="patternname", default="Halation", type="string", help="set Quantum test pattern.\
                                                                                        default:halation")
    parser.add_option("-t", dest="timing", type="string", default="1080p60",help=\
                                                            "Set input timing[qdcode | all | random]\
                                                            default: 1080p60\
                                                            all: all input timing\
                                                            random: random input timing \
                                                            qdcode: the manual timing,eg,2160p30")

    parser.add_option("-s", dest="scaletiming", type="string", default="auto",help=\
                                                            "Set scale output timing.[qdcode | auto | bypass | random ].\
                                                            defalut:auto\
                                                            bypass: bypass\
                                                            auto: all support scale timing\
                                                            random: random output timing\
                                                            manual: manual output timing\
                                                            qdcode: the manual scale timing, eg, 2160p60")
    parser.add_option("-c", dest="colorspace", type="string", default="YCbCr444",help=\
                                                            "Set Quantum colorspace.[ RGB | YCbCr444 | YCbCr422 | YCbCr420]\
                                                            defalut:RGB")
    parser.add_option("-d", dest="deepcolor", type="string", default="8",help="Set Quantum deepcolor.[8 | 10 | 12]")
    parser.add_option("-r", dest="repetitions", type="string", default="1",help="Set the test loop repetitions")
    parser.add_option("-i", dest="interval", type="string", default="1",help="Set DUT switch time interval(Uint:second)")
    parser.add_option("--hdcp", dest="hdcp", type="string", default="None",help="Set Quantum out HDCP.[None | 14 | 22]")
    parser.add_option("--ignore", dest="ignore", type="string", default="None",help="Ignore specified HDMI protocal para, eg:VIC, AR,...")
    parser.add_option("--outport", dest="outport", type="string", default='HDMI', \
                                                             help="Set Quantum Device output port.[HDMI | HDBT]")
    parser.add_option("--inport", dest="inport", type="string", default='HDMI', \
                                                             help="Set Quantum Device input port.[HDMI | HDBT]")
    parser.add_option("--random", dest="random", type="string",help=\
                                                            "Random Switch Input/Output ports.[ input | output | all ]")
    parser.add_option("--ar", dest="aspectratio", type="string", default ="stretch", help=\
                                                            "Set DUT AspectRatio, default is stretch .[ maintain | stretch ]")
    parser.add_option("--skip", dest="skip", type="string", help=\
                                                            "Skip HDMI Protocal/Pattern Test .[ protocal | pattern ]")
    parser.add_option("--outcolor", dest="outcolorspace", type="string", default="RGB",help=\
                                                            "Set DUT colorspace.[ RGB | YCbCr444]\
                                                            defalut:RGB")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose out")
    options, args = parser.parse_args()
    #if not args:
        #parser.print_help()
        #exit(1)
    execute_test(options, args)

if __name__=="__main__":
    main()