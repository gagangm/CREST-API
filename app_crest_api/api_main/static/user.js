$(document).ready(function() {   
    
    $('#example').DataTable( {
        "searching": false,
        "paging":   false,

        ajax: "/auth/get_users",
        columns: [
            { data: "id" },
            { data: "email" },
            { data: "site_url" },
            {
                data:   "status",
                render: function ( data, type, row ) {
                    if ( type === 'display' ) {
                        if(row.status === true)
                            return '<input type="checkbox" class="editor-active" checked>';
                        else 
                            return '<input type="checkbox" class="editor-active">';
                    }
                    return data;
                }
            },
            { data:   "details",
                    render: function ( data, type, row ) {
//                     console.log(type);
                        if ( type === 'display' ) {
                            if(row.details === true)
                                return '<input type="button" class="popup" value="Details">';
                            else 
                                return '<input type="button" class="popup" value="Details">';
                        }
                        return data;
                }
            },
        ],
        rowCallback: function ( row, data ) {
    } 
} );
 
    $('#example').on( 'change', 'input.editor-active', function () {
    var table = $('#example').DataTable();
    // this row consists of curent checked user
    row = table.row($(this).closest('tr') ).data();
    status = $('.editor-active').prop('checked');
    if (status == "true"){
    // call your authenticate and then signup api call get api-key,and store status and api key in db 
        $.ajax({
        url: '/auth/authenticate',
        data:{'userid':1},
        type: 'GET',
        success:function(response)
        {
        resp = JSON.parse(response);
        token = resp['token'];
        console.log(token);
        sessionStorage.setItem('token',token);
        field = sessionStorage.getItem('token'); 
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
                $.ajax({
                url : api_server+'/signup',
                data: {'email_address': row.email ,'site_url': row.site_url},
                headers: {'Authorization': 'Bearer ' + token},
                type: 'POST',
                success:function(response)
                {
                    var apikey = response.api_key;
                    var data = {"status":status,"api_key":apikey,"userid":row.id};
                    console.log(data);
                    $.ajax({
                    url: '/auth/save_details',
                    data: data,
                    type: 'POST',
                    success:function(response)
                    {
                        console.log(response);
                    }
                    });    
                }
            });
            },
            error:function(data)
            {
                console.log(data);
            }
        });    
        }
    });    
  }
});

    $('#example').on('click','input.popup',function(){
    var table = $('#example').DataTable();
    // this row consists of curent checked user
    row = table.row($(this).closest('tr') ).data();
    $.ajax({
        url: '/auth/authenticate',
        data:{'userid':1},
        type: 'GET',
        success:function(response)
        {
        resp = JSON.parse(response);
        console.log(response);
        token = resp['token'];
        console.log(token);
        sessionStorage.setItem('token',token);
        field = sessionStorage.getItem('token');
            $.ajax({
                url : '/auth/get_subscriber_details',
                type: 'POST',
                data: {'token': token,'userid':row.id},
                success:function(response)
                {
                    console.log(response);
                    window.alert(response);
                },
                    error:function(data){
                        $('#show-json-result').html('');
                }
            });
        }
    });
});
    
$('#close').on('click', function() { 
    $('#box').destroy();
    });
          
});