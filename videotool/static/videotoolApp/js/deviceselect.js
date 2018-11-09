$.ajaxSetup({
    data:{csrfmiddlewaretoken:'{{ csrf_token }}'},
});

$(document).ready(function () {
    $("#submit").click(function () {
        var qdmode = document.getElementById('qdmodel').options[document.getElementById('qdmodel').selectedIndex].text;
        console.log(qdmode);
        $.ajax({
            type: 'POST',
            url: '/connection/',
            dataType: 'json',
            data: {'qdmodel':qdmode},
            success: function (ret) {
                $('#serialselect').empty()
                $('#serialselect').append("<option value="+ret.comName+">"+ret.comName+"</option>")
                 $.ajax({    //send another ajax query to show qd device's output signal and connectors
                //type: 'POST',
                url: '/qddeviceselect/',
                //dataType: 'json',
                //data: {'qdmodel':qdmode},
                success: function (ret) {
                    $('#QDOUTPUTSIGNAL').empty()
                    $('#QDINPUTSIGNAL').empty()
                    $('#QDOUTPUTCONNECTOR').empty()
                    $.each(ret.qdoutporttype,function(i,value){
                    $('#QDOUTPUTSIGNAL').append("<option value="+i+">"+value+"</option>")
                    $('#QDOUTPUTSIGNAL').attr('size',i+1)
                    
                    })
                    $.each(ret.qdinporttype,function(i,value){
                    
                    $('#QDINPUTSIGNAL').append("<option value="+i+">"+value+"</option>")
                    $('#QDINPUTSIGNAL').attr('size',i+1)
                    })
                    $.each(ret.qdoutconnector,function(i,value){
                    
                    $('#QDOUTPUTCONNECTOR').append("<option value="+i+">"+value+"</option>")
                    $('#QDOUTPUTCONNECTOR').attr('size',i+1)
                    })
                    }
                })
                 $.ajax({    //query qdpatterns
               
                url: '/qdpattern/',
               
                success: function (ret) {
                    $('#QDPATTERNS').empty()
                    $.each(ret.qdpatterns,function(i,value){
                        var temp = ret.pk[i]
                       
                    $('#QDPATTERNS').append("<option value="+ret.pk[i]+">"+value+"</option>")
                    
                    })
                    
                    $("#QDPATTERNS ").get(0).selectedIndex=0; 
                     console.log($("#QDPATTERNS").val())  //get the value of select list
                    }
                })
            }
        })
           
        var a = $("#ipaddress").val();
        var b = $("#username").val();
        var c = $("#password").val();
        console.log(a)
        $.ajax({
            type: 'post',
            url: '/showdevice/',
            data: {'ipaddress': a, 'username': b, 'password': c},
            dataType: 'json',
            success: function (ret) {
                //$('#deviceselect').remove()
                $('#deviceselect').empty()
                var arr = ret.device_number
               
                $.each(ret.device_name, function (i, value) {
                   
                    var temp1 = value
                    var temp2 = ret.device_number[i]
                    var temp3 = temp2+'----'+temp1
                    $('#deviceselect').append("<option value="+i+">"+temp3+"</option>")
                    $('#deviceselect').attr('size',i+1)
                });
                //$('#mydiv').append(data.device_number[0]+'<br>');
            }
        });
    })

    $('#deviceselect').click(function () {
        console.log($("#deviceselect").find("option:selected").text())
        $.ajax({
            type: 'get',
            url: '/querydevicein/',
            data: {'devicename':$("#deviceselect").find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#porttypeselect_in').empty()
                $('#devicenumber').attr('value',ret.returnedname) 
                $.each(ret.porttype, function (i, value) {
                    $('#porttypeselect_in').append("<option value="+i+">"+value+"</option>")
                    $('#porttypeselect_in').attr('size',i+1)
                })
                $.ajax({  //after option items loaded, default is first one and we query input portnumbers right now
                    type: 'get',
                    url: '/queryportin/',
                    data: {'portnamein':$("#porttypeselect_in").find("option:selected").text()},
                    dataType: 'json',
                    success: function (ret) {
                        $('#portnumberselect_in').empty()
                        $.each(ret.portnumberselect_in, function (i, value) {
                            $('#portnumberselect_in').append("<option value="+i+">"+value+"</option>")
                            $('#portnumberselect_in').attr('size',i+1)
                        })
                    }
                })
                
               //because first ajax will cause write cache in file, so we put this ajax to here, after //that ajax successly done
                $.ajax({
                            type: 'get',
                            url: '/querydeviceout/',
                            data: {'devicename':$("#deviceselect").find("option:selected").text()},
                            dataType: 'json',
                            success: function (ret) {
                                $('#porttypeselect_out').empty()
                                $.each(ret.porttype, function (i, value) {
                                    $('#porttypeselect_out').append("<option value="+i+">"+value+"</option>")
                                    $('#porttypeselect_out').attr('size',i+1)
                                })
                                $.ajax({//after option items loaded, default is first one and we query out portnumbers right now
                                    type: 'get',
                                    url: '/queryportout/',
                                    data: {'portnameout':$("#porttypeselect_out").find("option:selected").text()},
                                    dataType: 'json',
                                    success: function (ret) {
                                        $('#portnumberselect_out').empty()
                                        $.each(ret.portnumberselect_out, function (i, value) {
                                            $('#portnumberselect_out').append("<option value="+i+">"+value+"</option>")
                                            $('#portnumberselect_out').attr('size',i+1)
                                        })
                                        $.ajax({//this ajax is for timing in refresh
                                                type: 'get',
                                                url: '/querytimingin/',
                                                data: {'portnamein':$("#porttypeselect_in").find("option:selected").text(),'portnumberin':$("#portnumberselect_in").find("option:selected").text(),'QDOUTPUTFILTER':$('#QDOUTPUTFILTER').find("option:selected").text()},
                                                dataType: 'json',
                                                success: function (ret) {
                                                    $('#timingselect_in').empty()
                                                    $.each(ret.timingselect_in, function (i, value) {
                                                        $('#timingselect_in').append("<option value="+ret.timingselect_in_id[i]+">"+value+"</option>")
                                                        //$('#timingselect_in').attr('size',i+1)
                                                    })
                                                }
                                            })
                                        $.ajax({//this ajax is for timing out refresh
                                                type: 'get',
                                                url: '/querytimingout/',
                                                data: {'portnameout':$("#porttypeselect_out").find("option:selected").text(),'portnumberout':$("#portnumberselect_out").find("option:selected").text(),'QDOUTPUTFILTER':$('#QDOUTPUTFILTER').find("option:selected").text()},
                                                dataType: 'json',
                                                success: function (ret) {
                                                    $('#timingselect_out').empty()
                                                    $.each(ret.timingselect_out, function (i, value) {
                                                        $('#timingselect_out').append("<option value="+ret.timingselect_out_id[i]+">"+value+"</option>")
                                                        //$('#timingselect_out').attr('size',i+1)
                                                    })
                                                }
                                            })    
                                        }
                                    })
                            }
                        })               
            }
        })

        
})

    $('#porttypeselect_in').click(function () {
        console.log('xxxxx')
        console.log($("#deviceselect").find("option:selected").text())
        $.ajax({
            type: 'get',
            url: '/queryportin/',
            data: {'portnamein':$("#porttypeselect_in").find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#portnumberselect_in').empty()
                $.each(ret.portnumberselect_in, function (i, value) {
                    $('#portnumberselect_in').append("<option value="+i+">"+value+"</option>")
                    $('#portnumberselect_in').attr('size',i+1)
                })
            }
        })
    })
    /* $('#QDPATTERNS').click(function () {
         $('#ipaddress1').attr('value','hehehhe') 
         $('#username1').attr('value','hahah') 
        console.log($("#QDPATTERNS").val())  //get the value of select list
        console.log($('#timingselect_in').val()) 
        var ret = {'hehe':[1,2,3,4]}
        var hehe = 'hehe'
        myfunction('#colorrange',ret,hehe)
    })
    function myfunction(id,ret,hehe){
       // alert('hello world!')
       $(id).empty()
       $.each(ret.hehe, function (i, value) {
                    $(id).append("<option value="+i+">"+value+"</option>")
                    $(id).attr('size',i+1)
                })
    } */
    
    $('#porttypeselect_out').click(function () {
        $.ajax({
            type: 'get',
            url: '/queryportout/',
            data: {'portnameout':$("#porttypeselect_out").find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#portnumberselect_out').empty()
                $.each(ret.portnumberselect_out, function (i, value) {
                    $('#portnumberselect_out').append("<option value="+i+">"+value+"</option>")
                    $('#portnumberselect_out').attr('size',i+1)
                })
            }
        })
    })
    $('#QDOUTPUTFILTER').click(function(){
      $.ajax({
            type: 'get',
            url: '/querytimingin/',
            data: {'portnamein':$("#porttypeselect_in").find("option:selected").text(),'portnumberin':$("#portnumberselect_in").find("option:selected").text(),'QDOUTPUTFILTER':$('#QDOUTPUTFILTER').find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#timingselect_in').empty()
                $.each(ret.timingselect_in, function (i, value) {

                    $('#timingselect_in').append("<option value="+ret.timingselect_in_id[i]+">"+value+"</option>")
                    //$('#timingselect_in').attr('size',i+1)
                })
            }
        }) 
      $.ajax({
            type: 'get',
            url: '/querytimingout/',
            data: {'portnameout':$("#porttypeselect_out").find("option:selected").text(),'portnumberout':$("#portnumberselect_out").find("option:selected").text(),'QDOUTPUTFILTER':$('#QDOUTPUTFILTER').find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#timingselect_out').empty()
                $.each(ret.timingselect_out, function (i, value) {
                    $('#timingselect_out').append("<option value="+ret.timingselect_out_id[i]+">"+value+"</option>")
                    //$('#timingselect_out').attr('size',i+1)
                })
            }
        })  
    })
    $('#portnumberselect_in').click(function () {
        console.log('xxxxx')
        console.log($("#deviceselect").find("option:selected").text())
        $.ajax({
            type: 'get',
            url: '/querytimingin/',
            data: {'portnamein':$("#porttypeselect_in").find("option:selected").text(),'portnumberin':$("#portnumberselect_in").find("option:selected").text(),'QDOUTPUTFILTER':$('#QDOUTPUTFILTER').find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#timingselect_in').empty()
                $.each(ret.timingselect_in, function (i, value) {

                    $('#timingselect_in').append("<option value="+ret.timingselect_in_id[i]+">"+value+"</option>")
                    //$('#timingselect_in').attr('size',i+1)
                })
            }
        })
    })
    $('#portnumberselect_out').click(function () {
        console.log('xxxxx')
        console.log($("#deviceselect").find("option:selected").text())
        $.ajax({
            type: 'get',
            url: '/querytimingout/',
            data: {'portnameout':$("#porttypeselect_out").find("option:selected").text(),'portnumberout':$("#portnumberselect_out").find("option:selected").text()},
            dataType: 'json',
            success: function (ret) {
                $('#timingselect_out').empty()
                $.each(ret.timingselect_out, function (i, value) {
                    $('#timingselect_out').append("<option value="+ret.timingselect_out_id[i]+">"+value+"</option>")
                    //$('#timingselect_out').attr('size',i+1)
                })
            }
        })
    })
    $('#submit1').click(function () {
        
        var ip = $('#ipaddress').val()
        var username = $('#username').val()
        var passwordd = $('#password').val()
        var porttypeselect_in = $('#porttypeselect_in').find("option:selected").text()
        var portnumberselect_in = $('#portnumberselect_in').val()
        var timingselect_in = $('#timingselect_in').val()
        
        var porttypeselect_out = $('#porttypeselect_out').find("option:selected").text()
        var portnumberselect_out = $('#portnumberselect_out').val()
        var timingselect_out = $('#timingselect_out').val()
        
        var QDOUTPUTSIGNAL = $('#QDOUTPUTSIGNAL').find("option:selected").text()
        var QDOUTPUTCONNECTOR = $('#QDOUTPUTCONNECTOR').find("option:selected").text()
        var QDINPUTSIGNAL = $('#QDINPUTSIGNAL').find("option:selected").text()
        
        var devicenumber = $('#devicenumber').val()
        var portt = $('#portt').val()
        var system = $('#system').val()
        
        var QDOUTPUTFILTER = $('#QDOUTPUTFILTER').val()
        var colorrange = $('#colorrange').val()
        var samplingmode = $('#samplingmode').val()
        var saclertype = $('#saclertype').val()
        var RX_Video_Timing = $('#RX_Video_Timing').val()
        var TX_Video_Timing = $('#TX_Video_Timing').val()
        
        var QDPATTERNS = $('#QDPATTERNS').val()
        
        
        
        
        var sendout = {'ip':ip,'username':username,'passwordd':passwordd,'porttypeselect_in':porttypeselect_in,'portnumberselect_in':portnumberselect_in,
        'timingselect_in':JSON.stringify(timingselect_in),'porttypeselect_out':porttypeselect_out,'portnumberselect_out':portnumberselect_out,'timingselect_out':JSON.stringify(timingselect_out),'QDOUTPUTFILTER':QDOUTPUTFILTER,'colorrange':colorrange,'samplingmode':samplingmode,'saclertype':saclertype,'RX_Video_Timing':RX_Video_Timing,'TX_Video_Timing':TX_Video_Timing,
        'QDOUTPUTSIGNAL':QDOUTPUTSIGNAL,'QDOUTPUTCONNECTOR':QDOUTPUTCONNECTOR,'QDINPUTSIGNAL':QDINPUTSIGNAL,'devicenumber':devicenumber,'portt':portt,'system':system,
        'QDPATTERNS':QDPATTERNS}
        console.log('submit1')
        console.log(sendout)
        
        //$(this).css({'background-color':'red'});
        
        
        $.ajax({
            type: 'get',
            url: '/receive_submit/',
            data: sendout,
            dataType: 'json',
            success: function (ret) {
                 $('#submit1').css({'background-color':'green'});
                }
            
        })
    })
});

















