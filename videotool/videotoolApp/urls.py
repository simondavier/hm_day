from django.conf.urls import url
from . import views

urlpatterns = [
    url('^connection/$', views.connection, name='connection'),
    url('^showtest/$',views.showtest, name='showtest'),
    url('^showdevice/$',views.showdevice, name='showdevice'),
    url('^addresolution/$',views.addresolution, name='addresolution'),
    url('^querydevicein/$',views.querydevicein, name='querydevicein'),
    url('^querydeviceout/$',views.querydeviceout, name='querydeviceout'),
    url('^queryportin/$',views.queryportin, name='queryportin'),
    url('^queryportout/$',views.queryportout, name='queryportout'),
    url('^qddeviceselect/$',views.qddeviceselect,name='qddeviceselect'),

]