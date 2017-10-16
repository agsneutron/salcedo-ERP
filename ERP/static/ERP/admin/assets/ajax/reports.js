/**
 * Created by bamaa on 14/09/17.
 */
$(document).on('ready', function() {
    /*
     Only do the cleanup if the field didn't contain a value already
     this is used for the edit form
     */
    get_Projects();
    $('#get_report_AFI').on('click',Get_Financial_Report);
    $('#get_report_AFF').on('click',Get_Physical_Financial);

});

function get_Projects(){

     $.ajaxSetup(
        {
            beforeSend: function(xhr, settings) {
                if(settings.type == "POST")
                    xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
                if(settings.type == "GET")
                    xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
            }
        }
    );

    // Get an Oauth2 access token and then do the ajax call, because SECURITY
  /*  $.get('/obras/register_by_token', function(ans) {
        var ajaxData = { access_token: ans.access_token};
        //alert(ans.access_token);*/
        $.ajax({
            url: '/erp/api/project_list',
            type: 'get',
            success: function(data) {
                set_Projects(data);

            },
            error: function(data) {
                var message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')
            }
        });

}

function set_Projects(data){
    clearControl("project_id_AFI");
    for (var i = 0; i < data.length; i++) {
        $("select#project_id_AFI").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreProyecto +
            '</option>'
        );
    }
    clearControl("project_id_AFF");
    for (var i = 0; i < data.length; i++) {
        $("select#project_id_AFF").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreProyecto +
            '</option>'
        );
    }
}


function clearControl(idcontrol) {
    
    $('select#'+idcontrol)
        .empty()
        .append('<option value>  Seleccione... </option>');
    
}


function Get_Financial_Report(){
    var project_id = $('select#project_id_AFI').find('option:selected').val();
    /*var detail_level = $('select#detail_level').find('option:selected').val();*/

    if (project_id != "" /*&& detail_level.toString()!= ""*/ ) {
        window.open("/reporting/get_financial_report?project_id=" + parseInt(project_id) /*+ "&detail_level="*/ /*+ detail_level.toString()*/);
    }
    else{
        alert("Para generar el reporte debe seleccionar un Proyecto");
    }
}

function Get_Physical_Financial(){
    var project_id = $('select#project_id_AFF').find('option:selected').val();
    

    if (project_id != "") {
        window.open("/reporting/get_physical_financial_advance_report?project_id=" + parseInt(project_id));
    }
    else{
        alert("Para generar el reporte debe seleccionar un Proyecto");
    }
}