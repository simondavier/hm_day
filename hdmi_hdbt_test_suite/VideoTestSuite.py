#!/usr/bin/env python
# -*- coding: utf-8 -*-

import quantum780_operation as qdoperation
import switchconfig_operation as switchconfig
import telnet_operation as telnet
import random
import os
import time
#import logging as log
#log.basicConfig(filename=logname, filemode="w", level=log.logger.info, format="[%(asctime)s]%(name)s:%(levelname)s:%(message)s")
import logger as log
from optparse import OptionParser
#log.disable(log.logger.info) #disable log

SWITCHCONFIG = "ConfigResolutionData.xlsx"
logname = ".\\log\\" + time.strftime("%Y%m%d_%H%M%S") + ".log"
log = log.Logger(logname)

def execute_test(cmdoptions, cmdargs):
    """
    Execute the test;
    :param cmdoptions:
    :param cmdargs:
    :return:
    """
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
    tnswitch = telnet.TelnetApp(config_d['SwitchIP'],config_d['SwitchUsername'],config_d['SwitchPassword'])
    swcregconf = switchconfig.SwitchConfigOperation(filename, 0)
    qd = qdoperation.Quantum780Operation()
    #inportlist = {'HDMI1':'1','HDMI2':'2']
    inportdic = init_port(config_d['InputPortType'])
    log.logger.info("The input port type is:%s."% inportdic)
    #outportlist = ['HDMI1':'1','HDMI2':'2'}
    outportdic = init_port(config_d['OutputPortType'])
    log.logger.info("The output port type is:%s."% outportdic)

    #Test Step:
    #Initialize QD generator
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
    tn.send_thor_cmd(config_d['SutDPS'], cmd_dut)
    tnswitch.send_thor_cmd(config_d['SwitchDPS'], cmd_sw)
    log.logger.info("Testing begin...")
    repetitions = int(cmdoptions.repetitions)
    log.logger.info("The inputlist is %s" % get_inputlist(swcregconf, cmdoptions.timing))
    while(repetitions): #execute repetions
        for qdcode in get_inputlist(swcregconf, cmdoptions.timing):
            log.logger.info("The current input timing is %s" % qdcode)
            #Set input timing
            qd.sent_qd_generator(qdcode)
            #Check the input timing
            check_input_timing(qd,qdcode,swcregconf)
            #Set Dut switch paraeters, paser "--random";
            if cmdoptions.random != None:
                time.sleep(cmdoptions.interval)
                cmd_dut,cmd_sw = rand_switch_port(cmdoptions.random, inportdic, outportdic )
                log.logger.info("Switch the DUT port is: %s" % cmd_dut)
                tn.send_thor_cmd(config_d['SutDPS'], cmd_dut)
                log.logger.info("Switch the Switch port is: %s" % cmd_sw)
                tnswitch.send_thor_cmd(config_d['SwitchDPS'], cmd_sw)
            #If bypass, Yes:dectected；Not:set output timing
            if 'bypass' == cmdoptions.scaletiming:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                #Set DUT output: bypass；
                tn.send_thor_cmd(config_d['SutDPS'],'VIDOUT_SCALE-BYPASS')
                #Set QD input port
                log.logger.info("Set QD analyze port!")
                qd.set_input_signal(0) #HDMI
                #Check the output
                check_output_timing(qd,qdcode,swcregconf)
            elif 'all'== cmdoptions.scaletiming or 'random'==cmdoptions.scaletiming:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                for scalercode in get_outputlist(swcregconf, cmdoptions.scaletiming):
                    #"for"  set aspect Ratio

                    log.logger.info("Set Scaler Out timing to %s!" % scalercode)
                    # set scaler to auto
                    tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-auto')
                    # set qd input port
                    log.logger.info("Set QD analyze port!")
                    qd.set_input_signal(0) #input hdmi
                    # write edid
                    write_edid(swcregconf, scalercode, edidfile, qd)
                    # check output paras
                    check_output_timing(qd,scalercode,swcregconf)
            else:
                log.logger.info("The scaler mode is %s" % cmdoptions.scaletiming)
                log.logger.info("Set Scaler Out timing to %s!" % cmdoptions.scaletiming)
                scalercode = cmdoptions.scaletiming
                # set scaler to manual
                tn.send_thor_cmd(config_d['SutDPS'], 'vidout_scale-manual')
                # set scaler output timing
                code = swcregconf.getTimingExpect(scalercode)
                #write edid to sink
                #write_edid(swcregconf, scalercode, edidfile, qd)
                #VIDOUT_RES_REF
                cmd=''.join('VIDOUT_RES_REF-'+code['HRES']+'x'+code['VRES']+','+str(int(float(code['VRAT']))))
                log.logger.info("The manual scaler timing out is %s" % cmd)
                tn.send_thor_cmd(config_d['SutDPS'], cmd)
                #Check output paras
                check_output_timing(qd,scalercode,swcregconf)
        repetitions = repetitions-1
    log.logger.info("All Test Completed!")

def init_port(porttype):
    dic = {}
    portlist = porttype.split(',')
    for opt in portlist:
        dic[opt.split(':')[0]] = opt.split(':')[1]
    return dic

def get_inputlist(swconfig, timingmode):
    """
    Get the input timing list
    :param swconfig:
    :param timingmode:
    :return:
    """
    if 'all' == timingmode:
        return swconfig.getSupportTimingCode(37)
    elif 'random' == timingmode:
        return random.choice(swconfig.getSupportTimingCode(37)).split()
    else:
        return timingmode.split()

def get_outputlist(swconfig, scalemode):
    """
    Get the output timing list
    :param swconfig:
    :param scalemode:
    :return:
    """
    if 'all' == scalemode:
        return  swconfig.getSupportTimingCode(39)
    elif 'random' == scalemode:
        return random.choice(swconfig.getSupportTimingCode(37)).split()
    else:
        return scalemode.split()

def check_input_timing(qd,qdcode,swcregconf):
    """
    Check the input timing
    :param qd:
    :param qdcode:
    :param swcregconf:
    :return:
    """
    log.logger.info("Get Expected Timing Result!")
    expect_input = swcregconf.getTimingExpect(qdcode)
    detect_input = qd.generator_timing_dump()
    log.logger.info("=The In Expected Para are:=")
    log.logger.info(expect_input)
    print("==Input Timing is: " + expect_input['HRES'] + "x" + expect_input['VRES'] + "@" + expect_input[
        'VRAT'] + "==")
    print("===================================")
    print("Input Timing" + expect_input['HRES'] + "x" + expect_input['VRES'] + "@" + expect_input['VRAT'] + " test is %s" \
          % swcregconf.compare_result(expect_input, detect_input))
    log.logger.info(
        "Input Timing" + expect_input['HRES'] + "x" + expect_input['VRES'] + "@" + expect_input['VRAT'] + " test is %s" \
        % swcregconf.compare_result(expect_input, detect_input))

def check_output_timing(qd,qdcode,swcregconf):
    """
    Check the output timing
    :param qd:
    :param qdcode:
    :param swcregconf:
    :return:
    """
    expect_output = swcregconf.getTimingExpect(qdcode)
    detect_output = qd.alyz_timing_dump()
    log.logger.info("=The Out Expected Para are:=")
    log.logger.info(expect_output)
    print("==Output Timing is: " + expect_output['HRES'] + "x" + expect_output['VRES'] + "@" + expect_output[
        'VRAT'] + "==")
    print("=====================================")
    print("Output Timing" + expect_output['HRES'] + "x" + expect_output['VRES'] + "@" + expect_output[
        'VRAT'] + " test is %s" \
          % swcregconf.compare_result(expect_output, detect_output))
    log.logger.info("Output Timing" + expect_output['HRES'] + "x" + expect_output['VRES'] + "@" + expect_output[
        'VRAT'] + " test is %s" \
          % swcregconf.compare_result(expect_output, detect_output))

def rand_switch_port(random, inportdic, outportdic):
    """
    random switch the DUT and Switcher
    :param random:
    :param inportdic:
    :param outportdic:
    :return:
    """
    if 'all' == random:
        #Random switch SUT in port
        inport = inportdic[random.choice(list(inportdic.keys()))]
        log.logger.info("The DUT IN port is: %s"%inport)
        #Random switch SUT out port
        outport = outportdic[random.choice(list(outportdic.keys()))]
        log.logger.info("The DUT OUT port is: %s"%outport)
        cmd_dut = ''.join('ci' + inport + 'o' + outport)
        log.logger.info("Set the DUT port is: %s" % cmd_dut)
        #Set Switch output
        cmd_sw = ''.join('ci'+outport+'oall')
        #log.logger.info("Set the Switch port is: %s" % cmd_sw)
    elif 'input' == random:
        # Random switch SUT in port, output default is first port
        inport = inportdic[random.choice(list(inportdic.keys()))]
        cmd_dut = ''.join('ci' + inport + 'o' + outportdic['HDMI1'])
        log.logger.info("The DUT IN port is: %s" % inport)
        #No output switch
        log.logger.info("OUTput has no change.")
        # Set Switch output
        cmd_sw = ''
    elif 'output' == random:
        #No switch SUT in port, input is the default
        log.logger.info("INput has no change.")
        outport = outportdic[random.choice(list(outportdic.keys()))]
        cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outport)
        log.logger.info("The DUT OUT port is: %s" % outport)
        cmd_sw = ''.join('ci' + outport + 'oall')
        #log.logger.info("Set the Switch port is: %s" % cmd_sw)
    else:
        cmd_dut = ''.join('ci' + inportdic['HDMI1'] + 'o' + outportdic['HDMI1'])
        cmd_sw = ''.join('ci' + outportdic['HDMI1'] + 'oall')
    return cmd_dut, cmd_sw

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

    parser.add_option("-s", dest="scaletiming", type="string", default="all",help=\
                                                            "Set scale output timing.[qdcode | all | bypass | random ].\
                                                            defalut:all(auto)\
                                                            bypass: bypass\
                                                            all: all support scale timing\
                                                            random: random output timing\
                                                            qdcode: the manual scale timing, eg, 2160p60")


    parser.add_option("-c", dest="colorspace", type="string", default="YCbCr444",help=\
                                                            "Set colorspace.[ RGB | YCbCr444 | YCbCr422 | YCbCr420]\
                                                            defalut:RGB")
    parser.add_option("-d", dest="deepcolor", type="string", default="8",help="Set deepcolor.[8 | 10 | 12]")
    parser.add_option("-r", dest="repetitions", type="string", default="1",help="Set the test loop repetitions")
    parser.add_option("-i", dest="interval", type="string", default="1",help="Set the switch time interval(Uint:second)")
    parser.add_option("--hdcp", dest="hdcp", type="string", default="None",help="Set HDCP.[None | 14 | 22]")
    parser.add_option("--outport", dest="outport", type="string", default='HDMI', \
                                                             help="Set Quantum Device output port.[HDMI | HDBT]")
    parser.add_option("--inport", dest="inport", type="string", default='HDMI', \
                                                             help="Set Quantum Device input port.[HDMI | HDBT]")
    parser.add_option("--random", dest="random", type="string",help=\
                                                            "Random Switch Input/Output.[ input | output | all ]")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="Verbose out")
    options, args = parser.parse_args()
    if not args:
        parser.print_help()
        exit(1)
    execute_test(options, args)

def process():
    import time
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

if __name__=="__main__":
    main()