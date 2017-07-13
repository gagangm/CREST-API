$(document).ready(function() {   
    
    $('#example1').DataTable( {
        "searching": false,
        "paging":   false,

        ajax: "/auth/get_pusers",
        columns: [
            { data: "id" },
            { data: "email" },
            { data: "api_server" },
            {
                data:   "status",
                render: function ( data, type, row ) {
                    if ( type === 'display' ) {
                        if(row.status === true)
                            return '<input type="checkbox"  class="editor-active" checked>';
                        else 
                            return '<input type="checkbox" class="editor-active">';
                    }
                    return data;
                }
            },
        ],
        rowCallback: function ( row, data ) {
    } 
  });
});
 
 $('#examples').on( 'change', 'input.editor-active', function () {
    var table = $('#examples').DataTable();
    // this row consists of curent checked user
    row = table.row($(this).closest('tr') ).data();
    status = $('.editor-active').prop('checked');
    if (status == "true"){
    // call your store status and api server in db
    {   
        var data = {"status":status, "api_server":apiserver, "puserid":row.id};
        $.ajax({
        url: '/auth/save_pdetails',
        data: data,
        type: 'POST',
        success:function(response)
        {
            console.log(response);
        }
        });    
    }
  }       
});

