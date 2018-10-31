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
                $.each(ret.porttype, function (i, value) {
                    $('#porttypeselect_in').append("<option value="+i+">"+value+"</option>")
                    $('#porttypeselect_in').attr('size',i+1)
                })
            }
        })

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

    $('#porttypeselect_out').click(function () {
        $.ajax({
            type: 'get',
            url: '/queryportout/',
            data: {'portnameout':$("#porttypeselect_out").find("option:selected").text(),'devicename':$("#deviceselect").find("option:selected").text()},
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

});

















