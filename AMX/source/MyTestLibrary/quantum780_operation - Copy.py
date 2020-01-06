#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial_connection as serial
import re,time

sc = serial.SerialConnection()
TESTPARAS = ['HRES', 'VRES', 'VRAT', 'VIC', 'HVIC', 'AR', 'SCAN', 'HTOT',
                 'HSPD', 'HSPW', 'HSPP', 'VTOT', 'VSPD', 'VSPW', 'VSPP']

class Quantum780Operation(object):
    def __init__(self):
        self.alyzDetected={}
        self.geneDetected={}

    def set_output_singal(self, sPort):
        """
        XVSI
        Select the ative video output interface
        :param port:
        :return:
        """
        if '2' == sPort:
            sc.send_cmd('XVSI 2') # DVI(Computer)
        elif '3' == sPort:
            sc.send_cmd('XVSI 3') # DVI(TV)
        elif '4' == sPort:
            sc.send_cmd('XVSI 4') #HDMI and HDBASET(Note)
        elif '8' ==sPort:
            sc.send_cmd('XVSI 8') #3GSDI
        elif '9' ==sPort:
            sc.send_cmd('XVSI 9') #Analog YPbPr or RGB
        elif '10' == sPort:
            sc.send_cmd('XVSI 10') # DisplayPort
        else:
            print("Unknown output signal！")

    def get_output_singal(self, port):
        """
        XVSI?
        Get the ative video output interface
        :param port:
        :return:
        """
        return sc.send_cmd('XVSI?')

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
            sc.send_cmd('HDBG 0')
        elif '1' == sConnector:
            sc.send_cmd('HDBG 1')
        else:
            print("Unknown output connector!")

    def get_output_hdbaset(self):
        """
        HDBG?
        Get HDBG?
        :return:
        """
        return sc.send_cmd('HDBG?')

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
        if '0' == sPort:
            sc.send_cmd('XVAI 0')
        elif '1' == sPort:
            sc.send_cmd('XVAI 1')
        elif '3' == sPort:
            sc.send_cmd('XVAI 3')
        else:
            print("Unknown input signal！")

    def get_input_signal(self):
        """
        XVAI?
        Get XVAI?
        :return:
        """
        return sc.send_cmd('XVAI?')

    def active_all(self):
        """
        ALLU
        Acivates a change to the video output
        :return:
        """
        sc.send_cmd('ALLU')

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
            sc.send_cmd('DVQM 0')
        elif '1' == opt:
            sc.send_cmd('DVQM 1')
        elif '2' == opt:
            sc.send_cmd('DVQM 2')
        else:
            print("Unknown color range!")

    def get_colorrange(self):
        """
        DVQM?
        Get DVQM?
        :return:
        """
        return sc.send_cmd('DVQM?')

    def set_samplingmode(self,opt):
        """
        DVSM
        Sets the digital video sampling mode, applies only for HDMI
        0 - RGB(4:4:4)
        2 - YCbCr(4:2:2)
        4 - YCbCr(4:4:4)
        :param opt:
        :return:
        """
        if '0' == opt:
            sc.send_cmd('DVSM 0')
        elif '2' == opt:
            sc.send_cmd('DVSM 2')
        elif '4' == opt:
            sc.send_cmd('DVSM 4')
        else:
            print("Unknown color samplemode!")

    def get_samplingmode(self):
        """
        DVSM?
        :return:
        """
        return sc.send_cmd('DVSM?')

    def set_videotype(self, opt):
        """
        DVST
        Sets the digital video type. Applies only for HDMI
        10 - RGB
        14 - YCbCr
        :return:
        """
        if '10' == opt:
            sc.send_cmd('DVST 10')
        elif '14' == opt:
            sc.send_cmd('DVST 14')
        else:
            print("Unknown video type!")

    def get_videotype(self):
        """
        DVST?
        :return:
        """
        return sc.send_cmd('DVST?')

    def load_testpattern(self, name):
        """
        IMGL
        Loads an image(pattern)
        :param name:
        pattern name;
        :return:
        """
        sc.send_cmd('IMGL '+name)

    def active_testpattern(self):
        """
        IMGU
        Active an image that has been loaded
        :return:
        """
        sc.send_cmd('IMGU')
    def get_testpattern(self):
        """
        IMGU?
        :return:
        """
        return sc.send_cmd('IMGU?')

    def load_format(self, name):
        """
        FMTL
        Loads a format
        :param name:
        Quantum format name
        :return:
        """
        sc.send_cmd('FMTL '+ name)

    def active_format(self):
        """
        FMTU
        Active a format that has been loaded
        :return:
        """
        sc.send_cmd('FMTU')

    def get_format(self):
        """
        Get current format
        :return:
        """
        return sc.send_cmd('FMTU?')

    def switch_hpformats(self, opt):
        """
        TOGG
        Enables or disables hot plug formats
        :param opt:
        0 = disable
        1 = enable
        :return:
        """
        sc.send_cmd('TOGG '+opt)

    def if_hpformats(self):
        """
        TOGG?
        :return:
        0 = disable
        1 = enable
        """
        return sc.send_cmd('TOGG?')

    def set_hppluse_width(self, width):
        """
        HPPW
        Sets the hot plug pluse width
        :param width:
        :return:
        """
        sc.send_cmd('HPPW '+str(width))

    def get_hppluse_width(self):
        """
        HPPW?
        :return:
        """
        return sc.send_cmd('HPPW?')

    def read_infoframes(self):
        """
        Read infoframes
        :return:
        """
        sc.send_cmd('IFAU')

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
            sc.send_cmd('IFAD? '+type)
        elif '82' == type:
            sc.send_cmd('IFAD? '+type)
        elif '83' == type:
            sc.send_cmd('IFAD? '+type)
        elif '84' == type:
            sc.send_cmd('IFAD? '+type)
        elif '85' == type:
            sc.send_cmd('IFAD? '+type)
        else:
            print("Unknown infoframe type!")

    def invoke_analyzer(self):
        """
        TMAU
        Invokes timing analyzer
        Before TMAX one or more commands, this command have to be executed
        :return:
        """
        sc.send_cmd('TMAU')

    def alyz_htot(self):
        """
        TMAX:HTOT?
        :return:
        """
        sc.send_cmd('TMAX:HTOT?')

    def gene_htot(self):
        """
        HTOT?
        :return:
        """
        sc.send_cmd('HTOT?')

    def alyz_hres(self):
        """
        TMAX:HRES?
        :return:
        """
        sc.send_cmd('TMAX:HRES?')

    def gene_hres(self):
        """
        HRES?
        :return:
        """
        sc.send_cmd('HRES?')

    def alyz_hspd(self):
        """
        TMAX:HSPD?
        :return:
        """
        sc.send_cmd('TMAX:HSPD?')

    def gene_hspd(self):
        """
        HSPD?
        :return:
        """
        sc.send_cmd('HSPD?')

    def alyz_hspp(self):
        """
        TMAX:HSPP?
        1 = Plus(positive)
        2 = Minus(negative)
        :return:
        """
        sc.send_cmd('TMAX:HSPP?')

    def gene_hspp(self):
        """
        HSPP?
        1 = Plus(positive)
        2 = Minus(negative)
        :return:
        """
        sc.send_cmd('HSPP?')

    def alyz_hspw(self):
        """
        TMAX:HSPW?
        :return:
        """
        sc.send_cmd('HSPW?')

    def gene_hspw(self):
        """
        HSPW?
        :return:
        """
        sc.send_cmd('HSPW?')

    def alyz_nbpc(self):
        """
        TMAX:NBPC?
        :return:
        """
        sc.send_cmd('TMAX:NBPC?')

    def gene_nbpc(self):
        """
        NBPC?
        :return:
        """
        sc.send_cmd('NBPC?')

    def alyz_scan(self):
        """
        TMAX:SCAN?
        1 = Progressive
        2 = Interlaced
        :return:
        """
        sc.send_cmd('TMAX:SCAN?')

    def gene_scan(self):
        """
        SCAN?
        1 = Progressive
        2 = Interlaced
        :return:
        """
        sc.send_cmd('SCAN?')

    def alyz_vrat(self):
        """
        TMAX:VRAT?
        :return:
        """
        sc.send_cmd('TMAX:VRAT?')

    def gene_vrat(self):
        """
        TMAX:VRAT?
        :return:
        """
        sc.send_cmd('VRAT?')

    def alyz_vtot(self):
        """
        TMAX:VTOT?
        :return:
        """
        sc.send_cmd('TMAX:VTOT?')

    def gene_vtot(self):
        """
        VTOT?
        :return:
        """
        sc.send_cmd('VTOT?')

    def alyz_vres(self):
        """
        TMAX:VRES?
        :return:
        """
        sc.send_cmd('TMAX:VRES?')

    def gene_vres(self):
        """
        VRES?
        :return:
        """
        sc.send_cmd('VRES?')

    def alyz_vspd(self):
        """
        TMAX:VSPD?
        :return:
        """
        sc.send_cmd('TMAX:VSPD?')

    def gene_vspd(self):
        """
        VSPD?
        :return:
        """
        sc.send_cmd('VSPD?')

    def alyz_vspp(self):
        """
        TMAX:VSPP?
        :return:
        """
        sc.send_cmd('TMAX:VSPP?')

    def gene_vspp(self):
        """
        VSPP?
        :return:
        """
        sc.send_cmd('VSPP?')

    def alyz_timing_dump(self):
        """
        Dump all TMAX commands result
        :return:
        A list of all TMAX commands result
        """
        for item in TESTPARAS:
            if item == 'VRAT':
                v = sc.send_cmd('VRAT?')
                self.alyzDetected[item] = ("%.2f" % float(v))
                print(self.alyzDetected[item])
                continue
            if item == 'AR':
                v = sc.send_cmd('XAVI:M?')
                if v == '1':
                    self.alyzDetected[item] = '4:3'
                    continue
                elif v == '2':
                    self.alyzDetected[item] = '16:9'
                    continue
                else:
                    self.alyzDetected[item] = 'Null'
                    continue
            if item == 'VIC':
                v = sc.send_cmd('XAVI:VIC?')
                self.alyzDetected[item] = v
                continue
            else:
                cmd = (item + '?')
                self.alyzDetected[item] = sc.send_cmd(cmd)
        print("============The Out Detected para are:============== ")
        print(self.alyzDetected)
        return self.alyzDetected

    def generator_timing_dump(self):
        """
        Dump all Generator timing result
        :return:
        A list of all Generator result
        """
        time.sleep(4)
        self.read_infoframes()
        out = sc.send_cmd_ar('IFAD? 82')
        for item in TESTPARAS:
            if item == 'AR':
                try:
                    self.geneDetected[item] = "".join(re.findall(r"AR:.*(\d.:\d)", out)[0])
                except:
                    self.geneDetected[item] = "Null"
                continue
            if item == 'VIC':
                self.geneDetected[item] = "".join(re.findall(r"Video ID:(.*)\(", out)).strip()
                continue
            cmd = ('TMAX:' + item + '?')
            self.geneDetected[item] = sc.send_cmd(cmd)
        print("============The In Detected para are:============== ")
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
        sc.send_cmd('NBPC '+depth)

    def load_edid(self, edidfile):
        """
        DIDL my720p.xml
        DIDU
        Loads an EDID file into memory in preparation to apply it to the Rx port with the DIDU command
        :return:
        """
        sc.send_cmd('DIDL '+edidfile)
        sc.send_cmd('DIDU')

    def apply_edid(self):
        """
        DIDU
        Applies an EDID file loaded with DIDL to the RX and issues a hot plug pulse
        Note: Can be used in conjnction with the HPPW command to produce hot plug pulses of varying widths
        :return:
        """
        sc.send_cmd('DIDL')

    def init_capture(self):
        """
        PDAX:CAPF
        Initiates the capture of a referrence frame for the Frame Compare test.
        :return:
        """
        sc.send_cmd('PDAX:CAPF')

    def cap_frame(self, num):
        """
        PDAX:FRMS
        Specifies the number of frames to capture during the Frame Compare test.
        :return:
        """
        sc.send_cmd('PDAX:FRMS '+num.__str__())

    def init_compare_frame(self):
        """
        PDAU
        Initates the capture of the number of frames specified by and compares thos frames with captured rference frame
        :return:
        """
        sc.send_cmd('PDAU')

    def get_errCount(self):
        """
        PDAX:ERRQ?
        Get the number of pixel errors that occured during the comparison
        :return:
        """
        sc.send_cmd('PDAX:ERRQ?')

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

    def write_edid_block1(self, block, edid):
        """

        :param block:
        1 = block1
        2 = block2
        :param edid:
        :return:
        """
        if '1' == block:
            sc.send_cmd('XDID 0 80 '+edid)
        elif '2' == block:
            sc.send_cmd('XDID 80 80 '+edid)
        else:
            print("Unknown edid block!")

'''if __name__ == '__main__':
    qdcon = Quantum780Operation()
    #print(qdcon.generator_timing_dump())
    print(qdcon.alyz_timing_dump())
    #print(qdcon.query_pixelErrCount(100))'''