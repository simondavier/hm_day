#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import quantum780_operation as qdoperation
import switchconfig_operation as switchconfig
import telnet_operation as telnet
import logger as log
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
    process()
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
    qd = qdoperation.Quantum780Operation()
    inportdic = init_port(config_d['InputPortType'])
    log.logger.info("The input port type is:%s."% inportdic)
    outportdic = init_port(config_d['OutputPortType'])
    log.logger.info("The output port type is:%s."% outportdic)
    # initialize the port;
    outport = config_d['SutDPS'].split(":")[1]
    #Test Step:
    #Ignore HDMI proctocal test parametres;
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
    cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outportdic['HDMI1'])
    cmd_sw = ''.join('ci'+outportdic['HDMI1']+'oall')
    inport = inportdic['HDMI1']
    inporttype = 'HDMI1'
    outport = outportdic['HDMI1']
    outporttype = 'HDMI1'
    tn.send_thor_cmd(config_d['SutDPS'], cmd_dut)
    tn.send_thor_cmd(config_d['SwitchDPS'], cmd_sw)
    log.logger.info("Hey,Testing Start......")
    repetitions = int(cmdoptions.repetitions)
    while(repetitions): #execute repetions
        for qdcode in get_timinglist(swcregconf, cmdoptions.timing, 37):
            log.logger.info("The current input timing is %s" % qdcode)
            #Set input timing
            qd.sent_qd_generator(qdcode)
            #If input skip protocal test
            if 'protocal' == cmdoptions.skip:
                pass
            else:
                #Check the input timing only
                if check_timing(qd, qdcode, swcregconf, 'input'):
                    INPCOUNT = INPCOUNT+1
                else:INFCOUNT = INFCOUNT+1

            #Set Dut switch paraeters, paser "--random";
            if cmdoptions.random != None:
                time.sleep(int(cmdoptions.interval))
                cmd_dut,cmd_sw, outport, outporttype, inporttype = rand_switch_port(cmdoptions.random, inportdic, outportdic)
                log.logger.info("The input port is %s" % inporttype)
                log.logger.info("The output port is %s" % outporttype)
                #Check if input port support HDBT Big 4K
                if is_hdbt_support(cmdoptions,qdcode,inporttype):
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
                set_qd_inputport(qd, outporttype)
                #if output skip protocal test
                if 'protocal' == cmdoptions.skip:
                    #check bypass pattern
                    pass
                elif 'pattern' == cmdoptions.skip:
                    #Check the output
                    if check_timing(qd,qdcode,swcregconf,'output'):
                        OUTPCOUNT = OUTPCOUNT+1
                    else:OUTFCOUNT = OUTFCOUNT+1
                else:
                    #Check the output
                    if check_timing(qd,qdcode,swcregconf,'output'):
                        OUTPCOUNT = OUTPCOUNT+1
                    else:OUTFCOUNT = OUTFCOUNT+1
                    #check bypass pattern
                    pass
            elif 'auto'== cmdoptions.scaletiming: #or 'random'==cmdoptions.scaletiming:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                for scalercode in get_timinglist(swcregconf, cmdoptions.scaletiming, 38):
                    #HDBT can not support 4096x2160@50/60 YCbCr/RGB input or output
                    if is_hdbt_support(cmdoptions,scalercode,outporttype):
                        pass
                    else:
                        continue
                    #"for"  set aspect Ratio
                    # To do sth
                    log.logger.info("Set Scaler Out timing to %s!" % scalercode)
                    # set scaler to auto
                    if cmdoptions.random != 'None':
                        newdps = config_d['SutDPS'].replace(":1:", ":" + outport + ":")
                        log.logger.info("The new SUT DPS is %s" % newdps)
                        tn.send_thor_cmd(newdps, 'vidout_scale-auto')
                    else:tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-auto')
                    # set qd input port
                    log.logger.info("Set QD analyze port!")
                    set_qd_inputport(qd, outporttype)
                    # write edid
                    write_edid(swcregconf, scalercode, edidfile, qd)
                    # if output skip protocal test
                    if 'protocal' == cmdoptions.skip:
                        # check pattern
                        pass
                    elif 'pattern' == cmdoptions.skip:
                        # check output paras
                        if check_timing(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                    else:
                        # check output paras
                        if check_timing(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                        # check pattern
                        pass

            else:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                #scalercode = cmdoptions.scaletiming
                for scalercode in get_timinglist(swcregconf, cmdoptions.scaletiming, 38):
                    # HDBT can not support 4096x2160@50/60 YCbCr/RGB input or output
                    if is_hdbt_support(cmdoptions, scalercode, outporttype):
                        pass
                    else:
                        continue
                    log.logger.info("Set Scaler Out timing to %s!" % scalercode)
                    # set scaler to manual
                    if cmdoptions.random != 'None':
                        #config_d['SutDPS'] = config_d['SutDPS'].replace(":1:", ":" + outport + ":")
                        newdps = config_d['SutDPS'].replace(":1:", ":" + outport + ":")
                        log.logger.info("The new SUT DPS is %s" % newdps)
                        #tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-manual')
                        tn.send_thor_cmd(newdps, 'vidout_scale-manual')
                    else:tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-manual')
                    # set scaler output timing
                    code = swcregconf.getTimingExpect(scalercode)
                    #write edid to sink
                    #write_edid(swcregconf, scalercode, edidfile, qd)
                    #VIDOUT_RES_REF
                    cmd=''.join('VIDOUT_RES_REF-'+code['HRES']+'x'+code['VRES']+','+str(round(float(code['VRAT']))))
                    log.logger.info("The manual scaler timing out is %s" % cmd)
                    tn.send_thor_cmd(newdps, cmd)
                    #Set QD input port
                    log.logger.info("Set QD analyze port!")
                    set_qd_inputport(qd, outporttype)
                    # if output skip protocal test
                    if 'protocal' == cmdoptions.skip:
                        # check pattern
                        pass
                    elif 'pattern' == cmdoptions.skip:
                        # check output paras
                        if check_timing(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                    else:
                        # check output paras
                        if check_timing(qd, scalercode, swcregconf, 'output'):
                            OUTPCOUNT = OUTPCOUNT + 1
                        else:
                            OUTFCOUNT = OUTFCOUNT + 1
                        # check pattern
                        pass
        repetitions = repetitions-1
    #Calculate all test result
    log.logger.info("OK,All Test Completed! Total: "+str(INPCOUNT+INFCOUNT+OUTPCOUNT+OUTFCOUNT)+" cases, "\
                    +str(INPCOUNT+OUTPCOUNT)+" was PASS, " +str(INFCOUNT+OUTFCOUNT)+" was FAIL!")
    log.logger.info("INPUT RESULT:"+str(INPCOUNT)+" is PASS, "+str(INFCOUNT)+" is FAIL. "\
                    "OUTPUT RESULT:"+str(OUTPCOUNT)+" is PASS, "+str(OUTFCOUNT)+" is FAIL")

def init_port(porttype):
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

def is_hdbt_support(cmdoptions, qdcode, porttype):
    if 'HDBT' in porttype:
        if qdcode == '2160p50w' or qdcode == '2160p60w':
            if cmdoptions.colorspace == 'RGB' or cmdoptions.colorspace == 'YCbCr444':
                log.logger.info("HDBT "+porttype+" can not support 4096x2160@50/60,RGB/YCbCr444!!!")
                return False
    return True

def set_qd_inputport(qd, outporttype):
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

def get_timinglist(swconfig, timingmode, col):
    if 'all' == timingmode or 'auto' == timingmode or 'manual' == timingmode:
        return swconfig.getSupportTimingCode(col)
    elif 'random' == timingmode:
        return random.choice(swconfig.getSupportTimingCode(col)).split()
    else:
        return timingmode.split()

def check_timing(qd, qdcode, swcregconf, inout):
    """
    Check the input timing
    :param qd:
    :param qdcode:
    :param swcregconf:
    :param inout:
    :return:
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

def rand_switch_port(rand, inportdic, outportdic):
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
        cmd_sw = ''.join('ci'+outport+'oall')
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
        cmd_sw = ''.join('ci' + outport + 'oall')
        #log.logger.info("Set the Switch port is: %s" % cmd_sw)
    else:
        cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outportdic['HDMI1'])
        cmd_sw = ''.join('ci' + outportdic['HDMI1'] + 'oall')
    return cmd_dut, cmd_sw, outport, outporttype, inporttype

def write_edid(swcregconf, scalercode, edidfile, qd):
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

def process():
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

def check_pattern():
    pass

def main():
    """
    :return:
    """
    usage = "usage: %prog [options] args"
    parser = OptionParser(usage)
    parser.add_option("-p", dest="patternname", default="colorbar", type="string", help="set test pattern.\
                                                                                        default:colorbar")
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
                                                            "Set colorspace.[ RGB | YCbCr444 | YCbCr422 | YCbCr420]\
                                                            defalut:RGB")
    parser.add_option("-d", dest="deepcolor", type="string", default="8",help="Set deepcolor.[8 | 10 | 12]")
    parser.add_option("-r", dest="repetitions", type="string", default="1",help="Set the test loop repetitions")
    parser.add_option("-i", dest="interval", type="string", default="1",help="Set the switch time interval(Uint:second)")
    parser.add_option("--hdcp", dest="hdcp", type="string", default="None",help="Set HDCP.[None | 14 | 22]")
    parser.add_option("--ignore", dest="ignore", type="string", default="None",help="Ignore specified HDMI protocal para, eg:VIC, AR,...")
    parser.add_option("--outport", dest="outport", type="string", default='HDMI', \
                                                             help="Set Quantum Device output port.[HDMI | HDBT]")
    parser.add_option("--inport", dest="inport", type="string", default='HDMI', \
                                                             help="Set Quantum Device input port.[HDMI | HDBT]")
    parser.add_option("--random", dest="random", type="string",help=\
                                                            "Random Switch Input/Output.[ input | output | all ]")
    parser.add_option("--ar", dest="aspectratio", type="string", default ="maintain", help=\
                                                            "Set AspectRatio .[ maintain | stretch ]")
    parser.add_option("--skip", dest="skip", type="string", help=\
                                                            "Skip HDMI Protocal/Pattern Test .[ protocal | pattern ]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose out")
    options, args = parser.parse_args()
    #if not args:
        #parser.print_help()
        #exit(1)
    execute_test(options, args)

if __name__=="__main__":
    main()