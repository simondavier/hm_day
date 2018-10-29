from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(QuantumDevice)
admin.site.register(QDoutport)
admin.site.register(Quantum2QDoutput)
admin.site.register(Resolution)
admin.site.register(Timing2QDoutport)
admin.site.register(AMX_SUT)
admin.site.register(Sutport)
admin.site.register(Sut2Sutinport)
admin.site.register(Sut2Sutouport)
admin.site.register(PR0808_input)
admin.site.register(PR0808_output)
admin.site.register(Sutinport2PR0808)
admin.site.register(Sutoutport2PR0808)
admin.site.register(Timing2PR0808input)
admin.site.register(Timing2PR0808output)
admin.site.register(CTP1301_input)
admin.site.register(CTP1301_output)
admin.site.register(Sutinport2CTP1301)
admin.site.register(Sutoutport2CTP1301)
admin.site.register(Timing2CTP1301input)
admin.site.register(Timing2CTP1301output)
