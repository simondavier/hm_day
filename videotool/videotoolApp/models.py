from django.db import models

# Create your models here.

#QD device model
class QuantumDevice(models.Model):
    qmodel = models.CharField(max_length=20)
    qfirmware = models.CharField(max_length=20)
    def __str__(self):
        print("%s in Qdsut models" % self.qmodel)

#Quantum device port model
class QDoutport(models.Model):
    qport = models.CharField(max_length=20)

#Quantum map to output port model
class Quantum2QDoutput(models.Model):
    quantum_model = models.IntegerField() #780E,980B
    qdport_type = models.IntegerField()  #VGA,HDMI,HDBASET,DVI


#Define Resolution Manager
class ResolutionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDelete=False)

#Resolution(Timming) model
class Resolution(models.Model):
    resObject=ResolutionManager()
    res = models.CharField(max_length=20)
    expres = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    edid = models.CharField(max_length=20)
    dtd = models.CharField(max_length=20)
    cvt = models.IntegerField()
    rb = models.CharField(max_length=20)
    date = models.CharField(max_length=20)
    dmtid = models.CharField(max_length=20)
    stdid = models.CharField(max_length=20)
    cvtid = models.CharField(max_length=20)
    vic = models.CharField(max_length=20)
    hvic = models.CharField(max_length=20)
    ar = models.CharField(max_length=20)
    htot = models.CharField(max_length=20)
    hres = models.CharField(max_length=20)
    hspd = models.CharField(max_length=20)
    hspw = models.CharField(max_length=20)
    hspp = models.CharField(max_length=20)
    scan = models.CharField(max_length=20)
    vrat = models.FloatField()
    vtot = models.CharField(max_length=20)
    vres = models.CharField(max_length=20)
    vspd = models.CharField(max_length=20)
    vspw = models.CharField(max_length=20)
    vspp = models.CharField(max_length=20)
    pclk = models.FloatField()
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        print("Resolution %s" % self.res)
    #define a method to create resolution object
    @classmethod
    def createResolution(cls, r_res, r_expres, r_code, r_edid, r_dtd,r_cvt, r_rb,r_date,r_dmtid,r_stdid,r_cvtid,r_vic,
                         r_hvic,r_ar,r_htot,r_hres,r_hspd,r_hspw,r_hspp,r_scan,r_vrat,r_vtot,r_vres,r_vspd,r_vspw,
                         r_vspp,r_pclk,isD=False):
        resolution = cls(res=r_res, expres=r_expres, code=r_code, edid=r_edid, dtd=r_dtd,cvt=r_cvt, rb=r_rb,date=r_date,
                         dmtid=r_dmtid,stdid=r_stdid,cvtid=r_cvtid,vic=r_vic,hvic=r_hvic,ar=r_ar,htot=r_htot,
                         hres=r_hres,hspd=r_hspd,hspw=r_hspw,hspp=r_hspp,scan=r_scan,vrat=r_vrat,vtot=r_vtot,
                         vres=r_vres,vspd=r_vspd,vspw=r_vspw,vspp=r_vspp,pclk=r_pclk,isDelete=isD)
        return resolution

#Resolution map to Quantum output
class Timing2QDoutport(models.Model):
    resolution = models.IntegerField()
    qdport = models.IntegerField()

#######define AMX sut ##################################
class AMX_SUT(models.Model):
    sModel = models.CharField(max_length=20)
    sFirmware = models.CharField(max_length=50)
    device_output = models.CharField(max_length=100)
    device_input = models.CharField(max_length=100)
    sutinport2device = models.CharField(max_length=100)
    sutoutput2device = models.CharField(max_length=100)
    timing2deviceinput = models.CharField(max_length=100)
    timing2deviceoutput = models.CharField(max_length=100)
    hasScaler = models.BooleanField(default=True)
    hasSwitch = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        print ("%s is in sutdata models" % self.sModel)
#Sut port type
class Sutport(models.Model):
    sport = models.CharField(max_length=20)
    def __str__(self):
        print ("%s is in sut port" % self.sport)
#SUT map to SUT input port:
class Sut2Sutinport(models.Model):
    ssut = models.IntegerField()
    ssutinport = models.IntegerField()
#SUT map to SUT output port;
class Sut2Sutouport(models.Model):
    ssut = models.IntegerField()
    ssutoutport = models.IntegerField()

#####################define PR0808 #############################
#PR0808 Input
class PR0808_input(models.Model):
    portname = models.CharField(max_length=20)
    inportnumber= models.IntegerField()
#PR0808 Output
class PR0808_output(models.Model):
    portname = models.CharField(max_length=20)
    outportnumber = models.IntegerField()
#PR08082Inport
class Sutinport2PR0808(models.Model):
    sutinport_id = models.IntegerField()
    pr_inportid = models.IntegerField()
#PR08082Outport
class Sutoutport2PR0808(models.Model):
    sutoutport_id = models.IntegerField()
    pr_outportid = models.IntegerField()
#Timing2 PR0808input
class Timing2PR0808input(models.Model):
    pr_inport = models.IntegerField()
    res = models.IntegerField()
#Timing2 PR0808output
class Timing2PR0808output(models.Model):
    pr_outport = models.IntegerField()
    res = models.IntegerField()

####################define CTP1301 ################################
#CTP1301 input
class CTP1301_input(models.Model):
    portname = models.CharField(max_length=20)
    inportnumber = models.IntegerField()
#CTP1301 output
class CTP1301_output(models.Model):
    portname = models.CharField(max_length=20)
    outportnumber = models.IntegerField()
#CTP13012Inport
class Sutinport2CTP1301(models.Model):
    sutinport_id = models.IntegerField()
    pr_inportid = models.IntegerField()
#CPT13012Outport
class Sutoutport2CTP1301(models.Model):
    sutoutport_id = models.IntegerField()
    pr_outportid = models.IntegerField()
#Timing2 CTP1301input
class Timing2CTP1301input(models.Model):
    pr_inport = models.IntegerField()
    res = models.IntegerField()
#Timing2 CTP1301output
class Timing2CTP1301output(models.Model):
    pr_outport = models.IntegerField()
    res = models.IntegerField()

#QD pattern
class Qdpattern(models.Model):
    qpattern = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        print ("%s was in QD" % self.qpattern)


