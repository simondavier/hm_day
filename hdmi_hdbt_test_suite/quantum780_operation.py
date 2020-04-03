#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial_connection as serial
import re,time
import logging as log
log.basicConfig(level=log.DEBUG,format="[%(asctime)s]%(name)s:%(levelname)s:%(message)s")

class Quantum780Operation(object):
    def __init__(self):
        self.sc = serial.SerialConnection()
        self.alyzDetected={}
        self.geneDetected={}
        self.TESTPARAS = ['HRES', 'VRES', 'VRAT', 'VIC', 'AR', 'SCAN', 'HTOT','HSPD', 'HSPW', 'HSPP', 'VTOT', 'VSPD', 'VSPW', 'VSPP']

    def get_version(self):
        """
        *IDN?
        :return:
        """
        return self.sc.send_cmd1('*IDN?')

    def set_output_singal(self, sPort):
        """
        XVSI
        Select the ative video output interface
        :param port:
        :return:
        """
        if '2' == sPort:
            self.sc.send_cmd('XVSI 2') # DVI(Computer)
        elif '3' == sPort:
            self.sc.send_cmd('XVSI 3') # DVI(TV)
        elif '4' == sPort:
            self.sc.send_cmd('XVSI 4') #HDMI and HDBASET(Note)
        elif '8' ==sPort:
            self.sc.send_cmd('XVSI 8') #3GSDI
        elif '9' ==sPort:
            self.sc.send_cmd('XVSI 9') #Analog YPbPr or RGB
        elif '10' == sPort:
            self.sc.send_cmd('XVSI 10') # DisplayPort
        else:
            raise("Unknown output signal！")

    def get_output_singal(self, port):
        """
        XVSI?
        Get the ative video output interface
        :param port:
        :return:
        """
        return self.sc.send_cmd('XVSI?')

    def set_output_hdbaset(self, sConnector):
        """
        HDBG
        Sets the active video output interface to HDBASET. Used with XVSI
        :param connector:
        0-HDMI
        1-HDBASET(Note)
        :return:
        """
        if '0' == sConnector:
            self.sc.send_cmd('HDBG 0')
        elif '1' == sConnector:
            self.sc.send_cmd('HDBG 1')
        else:
            raise("Unknown output connector!")

    def get_output_hdbaset(self):
        """
        HDBG?
        Get HDBG?
        :return:
        """
        return self.sc.send_cmd('HDBG?')

    def set_input_signal(self, sPort):
        """
        XVAI
         Select the ative video input interface
        :param port:
        0-HDMI
        1-HDBaseT
        3-DisplayPort
        :return:
        """
        if '0' == str(sPort):
            self.sc.send_cmd('XVAI 0')
        elif '1' == str(sPort):
            self.sc.send_cmd('XVAI 1')
        elif '3' == str(sPort):
            self.sc.send_cmd('XVAI 3')
        else:
            raise("Unknown input signal！")
        #self.sc.send_cmd('ALLU')

    def get_input_signal(self):
        """
        XVAI?
        Get XVAI?
        :return:
        """
        return self.sc.send_cmd('XVAI?')

    def active_all(self):
        """
        ALLU
        Acivates a change to the video output
        :return:
        """
        self.sc.send_cmd('ALLU')

    def set_colorrange(self, opt):
        """
        DVQM
        Sets or queries the digital video quantizing range. Applies only for HDMI
        :param opt:
        0 - 0-255(8 bit)
        1 - 1-254(8 bit)
        2 - 16-235(8 bit RGB)
            16-240(8 bit YCbCr)
        :return:
        """
        if '0' == opt:
            self.sc.send_cmd('DVQM 0')
        elif '1' == opt:
            self.sc.send_cmd('DVQM 1')
        elif '2' == opt:
            self.sc.send_cmd('DVQM 2')
        else:
            raise("Unknown color range!")
        self.sc.send_cmd('ALLU')

    def get_colorrange(self):
        """
        DVQM?
        Get DVQM?
        :return:
        """
        return self.sc.send_cmd('DVQM?')

    def set_samplingmode(self,opt):
        """
        DVSM
        Sets the digital video sampling mode, applies only for HDMI
        0 - RGB(4:4:4)
        2 - YCbCr(4:2:2)
        3 - YcbCr(4:2:0)
        4 - YCbCr(4:4:4)
        :param opt:
        :return:
        """
        if '0' == opt:
            self.sc.send_cmd('DVSM 0')
        elif '2' == opt:
            self.sc.send_cmd('DVSM 2')
        elif '3' == opt:
            self.sc.send_cmd('DVSM 3')
        elif '4' == opt:
            self.sc.send_cmd('DVSM 4')
        else:
            print("Unknown color samplemode!")
        self.sc.send_cmd('ALLU')

    def get_samplingmode(self):
        """
        DVSM?
        :return:
        """
        return self.sc.send_cmd('DVSM?')

    def set_videotype(self, opt):
        """
        DVST
        Sets the digital video type. Applies only for HDMI
        10 - RGB
        14 - YCbCr
        :return:
        """
        if '10' == opt:
            self.sc.send_cmd('DVST 10')
        elif '14' == opt:
            self.sc.send_cmd('DVST 14')
        else:
            raise("Unknown video type!")
        self.sc.send_cmd('ALLU')

    def get_videotype(self):
        """
        DVST?
        :return:
        """
        return self.sc.send_cmd('DVST?')

    def hdcp_alyzSwitch(self, opt):
        """
        CPAG
        Enable/Disable hdcp analyzer(Rx port)
        Set RX
        :param opt:
        0 = disable;
        1 = 1.4;
        2 = 2.2;
        :return:
        """
        #self.sc.send_cmd('DIDU')
        #time.sleep(5)
        self.sc.send_cmd('CPAG '+opt)

    def hdcp_generator(self, opt):
        """
        Generator hdcp 1.x, 2.x
        :param opt:
        0 = NoneHDCP
        1 = hdcp1.x
        2 = hdcp2.x
        :return:
        """
        self.sc.send_cmd('HDCP 0')
        if '0'== opt:
            self.sc.send_cmd('HDCP '+opt)
        elif '1' == opt:
            self.sc.send_cmd('HDCP '+opt)
        elif '2' == opt:
            self.sc.send_cmd('HDCP '+opt)
        else:
            raise ("Unknown hdcp parameters.")

    # def queryTX_hdcp(self, hdcpout):
    #     """
    #     Check Tx hdcp status, if off, then on
    #     :param opt:
    #     :return:
    #     """
    #     queryTX = self.get_tx_hdcp()
    #     print("Query TX hdcp disable(0) is %s, Quantum send is %s"%(queryTX,hdcpout))
    #     if "0" == queryTX:
    #         if "None" ==  hdcpout:
    #             self.sc.send_cmd('HDCP 0')
    #         elif "14" == hdcpout:
    #             self.sc.send_cmd('HDCP 1')
    #         elif "220" == hdcpout:
    #             self.sc.send_cmd('HDCP 2')
    #             self.sc.send_cmd('HSTG 0')
    #         elif "221" == hdcpout:
    #             self.sc.send_cmd('HDCP 2')
    #             self.sc.send_cmd('HSTG 1')
    #         else:
    #             raise ("Unknown hdcp parameters.")
    def queryTX_hdcp(self, hdcpout):
        """
        Check Tx hdcp status, if off, then on
        :param opt:
        :return:
        """
        queryTX = self.get_tx_hdcp()
        print("Query TX hdcp disable(0) is %s, Quantum send is %s"%(queryTX,hdcpout))
        while "0" == self.get_tx_hdcp():
            print("The hdcp will set to enable!")
            if "None" ==  hdcpout:
                self.sc.send_cmd('HDCP 0')
                break
            elif "14" == hdcpout:
                self.sc.send_cmd('HDCP 0')
                self.sc.send_cmd('HDCP 1')
                time.sleep(5)
            elif "220" == hdcpout:
                self.sc.send_cmd('HDCP 0')
                self.sc.send_cmd('HDCP 2')
                self.sc.send_cmd('HSTG 0')
                time.sleep(5)
            elif "221" == hdcpout:
                self.sc.send_cmd('HDCP 0')
                self.sc.send_cmd('HDCP 2')
                self.sc.send_cmd('HSTG 1')
                time.sleep(5)
        else:
            print("HDCP has been enabled now!")


    def hdcp_analyzer(self):
        """
        HDCP?
        Runs an HDCP autherication test on an HDMI sink device
        There is a bug on QD780E, When test hdcp2.2, return will be 9522.
        Note: After execute this command, the source will be discypted.
        :return:
        """
        res = str(self.sc.send_cmd('HDCP?'))
        if '0' == res:
            return True
        elif '9522' == res:
            return True
        else:
            return False

    def get_tx_hdcp(self):
        """
        Get Quantum output hdcp status
        :return: 0 off, not 0 on
        """
        return self.sc.send_cmd('CPGG?')

    def load_testpattern(self, name):
        """
        IMGL
        Loads an image(pattern)
        :param name:
        pattern name;
        :return:
        """
        self.sc.send_cmd('IMGL '+name)
        self.sc.send_cmd('IMGU')

    def active_testpattern(self):
        """
        IMGU
        Active an image that has been loaded
        :return:
        """
        self.sc.send_cmd('IMGU')
    def get_testpattern(self):
        """
        IMGU?
        :return:
        """
        return self.sc.send_cmd('IMGU?')

    def load_format(self, code):
        """
        FMTL
        Loads a format
        :param code:
        Quantum format name
        :return:
        """
        self.sc.send_cmd('FMTL '+ code)
        self.sc.send_cmd('FMTU')

    def active_format(self):
        """
        FMTU
        Active a format that has been loaded
        :return:
        """
        self.sc.send_cmd('FMTU')

    def get_format(self):
        """
        Get current format
        :return:
        """
        return self.sc.send_cmd('FMTU?')

    def switch_hpformats(self, opt):
        """
        TOGG
        Enables or disables hot plug formats
        :param opt:
        0 = disable
        1 = enable
        :return:
        """
        self.sc.send_cmd('TOGG '+opt)
        self.sc.send_cmd('ALLU')

    def if_hpformats(self):
        """
        TOGG?
        :return:
        0 = disable
        1 = enable
        """
        return self.sc.send_cmd('TOGG?')

    def set_hppluse_width(self, width):
        """
        HPPW
        Sets the hot plug pluse width
        :param width:
        :return:
        """
        self.sc.send_cmd('HPPW '+width)

    def get_hppluse_width(self):
        """
        HPPW?
        :return:
        """
        return self.sc.send_cmd('HPPW?')

    def read_infoframes(self):
        """
        Read infoframes
        :return:
        """
        self.sc.send_cmd('IFAU')

    def get_infoframes(self, type):
        """
        IFAD?
        Displays the contents of a specific type of infoframe
        :param type:
        -VSIF = 81
        - AVI = 82
        - SPD = 83
        - AUD = 84
        -MPEG = 85
        :return:
        """
        if '81' ==  type:
            self.sc.send_cmd('IFAD? '+type)
        elif '82' == type:
            self.sc.send_cmd('IFAD? '+type)
        elif '83' == type:
            self.sc.send_cmd('IFAD? '+type)
        elif '84' == type:
            self.sc.send_cmd('IFAD? '+type)
        elif '85' == type:
            self.sc.send_cmd('IFAD? '+type)
        else:
            raise("Unknown infoframe type!")

    def invoke_analyzer(self):
        """
        TMAU
        Invokes timing analyzer
        Before TMAX one or more commands, this command have to be executed
        :return:
        """
        self.sc.send_cmd('TMAU')

    def alyz_htot(self):
        """
        TMAX:HTOT?
        :return:
        """
        return self.sc.send_cmd('TMAX:HTOT?')

    def gene_htot(self):
        """
        HTOT?
        :return:
        """
        #str = self.sc.send_cmd('HTOT?')
        #return str+''
        return self.sc.send_cmd('HTOT?')

    def alyz_hres(self):
        """
        TMAX:HRES?
        :return:
        """
        return self.sc.send_cmd('TMAX:HRES?')

    def gene_hres(self):
        """
        HRES?
        :return:
        """
        return self.sc.send_cmd('HRES?')

    def alyz_hspd(self):
        """
        TMAX:HSPD?
        :return:
        """
        return self.sc.send_cmd('TMAX:HSPD?')

    def gene_hspd(self):
        """
        HSPD?
        :return:
        """
        return self.sc.send_cmd('HSPD?')

    def alyz_hspp(self):
        """
        TMAX:HSPP?
        1 = Plus(positive)
        2 = Minus(negative)
        :return:
        """
        return self.sc.send_cmd('TMAX:HSPP?')

    def gene_hspp(self):
        """
        HSPP?
        1 = Plus(positive)
        2 = Minus(negative)
        :return:
        """
        return self.sc.send_cmd('HSPP?')

    def alyz_hspw(self):
        """
        TMAX:HSPW?
        :return:
        """
        return self.sc.send_cmd('HSPW?')

    def gene_hspw(self):
        """
        HSPW?
        :return:
        """
        return self.sc.send_cmd('HSPW?')

    def alyz_nbpc(self):
        """
        TMAX:NBPC?
        :return:
        """
        return self.sc.send_cmd('TMAX:NBPC?')

    def gene_nbpc(self):
        """
        NBPC?
        :return:
        """
        return self.sc.send_cmd('NBPC?')

    def alyz_scan(self):
        """
        TMAX:SCAN?
        1 = Progressive
        2 = Interlaced
        :return:
        """
        return self.sc.send_cmd('TMAX:SCAN?')

    def gene_scan(self):
        """
        SCAN?
        1 = Progressive
        2 = Interlaced
        :return:
        """
        return self.sc.send_cmd('SCAN?')

    def alyz_vrat(self):
        """
        TMAX:VRAT?
        :return:
        """
        return self.sc.send_cmd('TMAX:VRAT?')

    def gene_vrat(self):
        """
        TMAX:VRAT?
        :return:
        """
        return self.sc.send_cmd('VRAT?')

    def alyz_vtot(self):
        """
        TMAX:VTOT?
        :return:
        """
        return self.sc.send_cmd('TMAX:VTOT?')

    def gene_vtot(self):
        """
        VTOT?
        :return:
        """
        return self.sc.send_cmd('VTOT?')

    def alyz_vres(self):
        """
        TMAX:VRES?
        :return:
        """
        return self.sc.send_cmd('TMAX:VRES?')

    def gene_vres(self):
        """
        VRES?
        :return:
        """
        return self.sc.send_cmd('VRES?')

    def alyz_vspd(self):
        """
        TMAX:VSPD?
        :return:
        """
        return self.sc.send_cmd('TMAX:VSPD?')

    def gene_vspd(self):
        """
        VSPD?
        :return:
        """
        return self.sc.send_cmd('VSPD?')

    def alyz_vspp(self):
        """
        TMAX:VSPP?
        :return:
        """
        return self.sc.send_cmd('TMAX:VSPP?')

    def gene_vspp(self):
        """
        VSPP?
        :return:
        """
        return self.sc.send_cmd('VSPP?')

    def generator_timing_dump(self):
        """
        generator_timing_dump
        Dump all generator commands result
        :return:
        A dic of all generator commands result
        """
        for item in self.TESTPARAS:
            if item == 'VRAT':
                v = self.sc.send_cmd('VRAT?')
                self.alyzDetected[item] = ("%.2f" % float(v))
                print(self.alyzDetected[item])
                continue
            if item == 'AR':
                v = self.sc.send_cmd('XAVI:M?')
                if v == '1':
                    self.alyzDetected[item] = '4:3'
                    #continue
                elif v == '2':
                    self.alyzDetected[item] = '16:9'
                    #continue
                else:
                    self.alyzDetected[item] = 'Null'
                continue
            if item == 'VIC':
                v = self.sc.send_cmd('XAVI:VIC?')
                self.alyzDetected[item] = v
                continue
            else:
                cmd = (item + '?')
                self.alyzDetected[item] = self.sc.send_cmd(cmd)
        print("============The Quantum Out Detected para are:============== ")
        print(self.alyzDetected)
        return self.alyzDetected

    def alyz_timing_dump(self):
        """
        alyz_timing_dump
        Dump all Generator timing result
        :return:
        A dic of all TMAX analyzer result
        """
        time.sleep(10)
        self.read_infoframes()
        out = self.sc.send_cmd_ar('IFAD? 82')
        for item in self.TESTPARAS:
            if item == 'AR':
                    #self.geneDetected[item] = "".join(re.findall(r"AR:.*(\d.:\d)", out)[0])
                self.geneDetected[item] = "".join(re.findall(r".*(\d.:\d)", out))
                #print("The AR was detected as:"+ self.geneDetected[item])
                if self.geneDetected[item]=='':
                    self.geneDetected[item] = "Null"
                continue
            if item == 'VIC':
                self.geneDetected[item] = "".join(re.findall(r"Video ID:(.*)\(", out)).strip()
                if '' == self.geneDetected[item]:
                    self.geneDetected[item]='0'
                continue
            cmd = ('TMAX:' + item + '?')
            self.geneDetected[item] = self.sc.send_cmd(cmd)
        print("============The Quantum In Detected para are:============== ")
        print(self.geneDetected)
        return self.geneDetected

    def set_colordepth(self, depth):
        """
        NBPC
        Sets the number of bits per component
        :param depth:
        8 - 8 bits per component
        10 - 10 bits per component
        12 - 12 bits per component
        :return:
        """
        self.sc.send_cmd('NBPC '+depth)

    def load_edid(self, edidfile):
        """
        DIDL my720p.xml
        DIDU
        Loads an EDID file into memory in preparation to apply it to the Rx port with the DIDU command
        :return:
        """
        self.sc.send_cmd('DIDL '+edidfile)
        self.sc.send_cmd('DIDU')

    def apply_edid(self):
        """
        DIDU
        Applies an EDID file loaded with DIDL to the RX and issues a hot plug pulse
        Note: Can be used in conjnction with the HPPW command to produce hot plug pulses of varying widths
        :return:
        """
        self.sc.send_cmd('DIDU')
        time.sleep(5)

    def init_capture(self):
        """
        PDAX:CAPF
        Initiates the capture of a referrence frame for the Frame Compare test.
        :return:
        """
        self.sc.send_cmd('PDAX:CAPF')

    def cap_frame(self, num):
        """
        PDAX:FRMS
        Specifies the number of frames to capture during the Frame Compare test.
        :return:
        """
        self.sc.send_cmd('PDAX:FRMS '+str(num))

    def init_compare_frame(self):
        """
        PDAU
        Initates the capture of the number of frames specified by and compares thos frames with captured rference frame
        :return:
        """
        self.sc.send_cmd('PDAU')
        time.sleep(7)

    def get_errCount(self):
        """
        PDAX:ERRQ?
        Get the number of pixel errors that occured during the comparison
        :return:
        """
        return self.sc.send_cmd('PDAX:ERRQ?')


    def query_pixelErrCount(self, number):
        """
        Compare the frame and get the error count
        :param num:
        num - Capture frames number
        :return:
        0 - no error
        other - error num counter
        """
        self.init_capture()
        self.cap_frame(number)
        self.init_compare_frame()
        return self.get_errCount()

    def get_pixel(self, x, y):
        """
        Return Pixel color.
        PDAX:PVAL?
        :param x: x coordinate
        :param y: y coordinate
        :return: a color list with Hex
        """
        res = self.sc.send_cmd_ar('PDAX:PVAL? '+x+' '+y)
        #print(res)
        return str(re.findall(r"0x[\w]+", res))


    def write_edid_block(self, block, edid):
        """

        :param block:
        0 = block0
        1 = block1
        :param edid:
        :return:
        """
        if '0' == block:
            self.sc.send_cmd('XDID 0 80 '+edid)
        elif '1' == block:
            self.sc.send_cmd('XDID 80 80 '+edid)
        else:
            print("Unknown edid block!")

    def sent_qd_generator(self, qdcode, pattern='', colorspace='', deepcolor='', outport='', hdcp=''):
        """
        sent Qd generator output;
        :param qdcode: timing qdcode;
        :param pattern: test pattern;
        :param colorspace: set color space;
        :param bit:  set color bitrate;
        :param outport: set output HDMI/HDBASET;
        :param hdcp: set hdcp; None,14,220,221
        :return:
        """
        #set QD output timing
        log.info("set QD output timing %s" % qdcode)
        self.load_format(qdcode)
        #set test pattern
        log.info("set test pattern %s"% pattern)
        if ""== pattern:
            pass
        else:self.load_testpattern(pattern)
        #set color space
        log.info("set color space %s" % colorspace)
        if ""==colorspace:
            pass
        else:
            self.set_videotype('14')
            if 'RGB' == colorspace:
                self.set_videotype('10')
                self.set_samplingmode('0')
            elif 'YCbCr444' == colorspace:
                self.set_samplingmode('4')
            elif 'YCbCr422' == colorspace:
                self.set_samplingmode('2')
            elif 'YCbCr420' == colorspace:
                self.set_samplingmode('3')
            else:
                raise ("Undefine colorspace.")
        #set bitrate
        log.info("set bitrate %s"% deepcolor)
        if ""==deepcolor:
            pass
        else:self.set_colordepth(deepcolor)
        #set output port HDMI/HDBASET
        log.info("set output port %s" % outport)
        if ""==outport:
            pass
        else:
            self.set_output_singal('4')
            if 'HDMI' == outport:
                self.set_output_hdbaset('0')
            elif 'HDBT' == outport:
                self.set_output_hdbaset('1')
            else: raise("Unknown output connector.")
        self.active_all()
        #set hdcp encrypt
        log.info("set hdcp encrypt hdcp %s" % hdcp)
        if "" == hdcp:
            pass
        else:
            #self.hdcp_alyzSwitch()
            if 'None' == hdcp:
                self.hdcp_generator('0')
            elif '14' == hdcp:
                self.hdcp_generator('1')
            elif '220' == hdcp: #type0
                self.hdcp_generator('2')
                self.sc.send_cmd('HSTG 0')
            elif '221' == hdcp: #type1
                self.hdcp_generator('2')
                self.sc.send_cmd('HSTG 1')
            else:raise ("Unknow hdcp key!")

    def close(self):
        self.sc.serial_close()


if __name__ == '__main__':
    qdcon = Quantum780Operation()
#     #print(qdcon.generator_timing_dump())
#     #print(qdcon.get_version())
#     #qdcon.init_capture()
#     #print(qdcon.alyz_timing_dump())
    res= qdcon.query_pixelErrCount(100)
    print(res)
    if '0' == res:
        print("pass")
    else:
        print("fail")
    #print(qdcon.get_errCount())
    print(qdcon.get_pixel('960','275'))
