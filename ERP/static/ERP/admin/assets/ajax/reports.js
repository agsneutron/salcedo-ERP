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
    $('#get_report_Estimacion').on('click',Get_Estimate_Report);
    $('#get_report_estimate_for_contract').on('click',Get_Estimate_For_Contract);
    $('#project_id_estimate_for_contract').on('change',get_Contractors);

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

function get_Contractors(){

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
    var project_id = $('select#project_id_estimate_for_contract').find('option:selected').val();
    // Get an Oauth2 access token and then do the ajax call, because SECURITY
  /*  $.get('/obras/register_by_token', function(ans) {
        var ajaxData = { access_token: ans.access_token};
        //alert(ans.access_token);*/
        $.ajax({
            url: '/erp/api/contractor_list?project_id='+parseInt(project_id),
            type: 'get',
            success: function(data) {
                set_Contractors(data);

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

    clearControl("project_id_Estimacion");
    for (var i = 0; i < data.length; i++) {
        $("select#project_id_Estimacion").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreProyecto +
            '</option>'
        );
    }

    clearControl("project_id_estimate_for_contract");
    for (var i = 0; i < data.length; i++) {
        $("select#project_id_estimate_for_contract").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreProyecto +
            '</option>'
        );
    }
}

function set_Contractors(data){

    clearControl("contratista_id_estimate_for_contract");
    for (var i = 0; i < data.length; i++) {
        $("select#contratista_id_estimate_for_contract").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreContratista +
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

function Get_Estimate_Report(){
    var project_id = $('select#project_id_Estimacion').find('option:selected').val();


    if (project_id != "") {
        window.open("/reporting/get_estimates_report?project_id=" + parseInt(project_id));
    }
    else{
        alert("Para generar el reporte debe seleccionar un Proyecto");
    }
}

function Get_Estimate_For_Contract(){
    var project_id = $('select#project_id_estimate_for_contract').find('option:selected').val();
    var contract_id = $('select#contratista_id_estimate_for_contract').find('option:selected').val();


    if (project_id != "") {
        window.open("/reporting/get_estimate_report_by_single_contractor?project_id="+ parseInt(project_id) + "&contractor_id="+ parseInt(contract_id));
    }
    else{
        alert("Para generar el reporte debe seleccionar un Proyecto");
    }
}
