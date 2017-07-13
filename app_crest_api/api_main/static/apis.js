$(document).ready(function() {
    var userid = $('#userid').val();
        console.log(userid);
    $.ajax({
            url: '/auth/get_api_server',
            data:{'userid':1},
            type: 'GET',
            success:function(response)
            {
                resp = JSON.parse(response);
                console.log();
                api_server = resp.api_server;
                sessionStorage.setItem('api_server',api_server);
            },
            error:function(data)
            {
                console.log(data);
            }
        }); 
    $.ajax({
            url: '/auth/authenticate',
            data:{'userid':userid},
            type: 'GET',
            success:function(response)
            {
                resp = JSON.parse(response);
                token = resp['token'];
                sessionStorage.setItem('token',token);
            },
            error:function(data)
            {
                console.log(data);
            }
        });    
});

         
                
                
