/**
 * Created by bamaa on 14/09/17.
 */

$(document).on('ready', function() {
    /*
     Only do the cleanup if the field didn't contain a value already
     this is used for the edit form
     */


});

function configura_segmentos(project_id){

     $('#projectID').val(project_id);

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
        var ajaxData = {project_id: project_id.toString()};
        $.ajax({
            url: '/erp/api/sections_by_project/',
            data: ajaxData,
            type: 'get',
            success: function(data) {
                alert("correcto");
                checkBoxesByProject(data);
            },
            error: function(data) {
                alert('error!! ' + data.status);
            }
        });

}

function checkBoxesByProject(respuesta){
    for (var i = 0; i < respuesta.length; i++) {
        if (respuesta[i].status==1){
            $(respuesta[i].shortSectionName).attr("checked");
        }
    }
}

function  guardaSegmento() {
        var seleccionados = $('input:checkbox:checked').map(function() {
            return this.value;
        }).get();
        var no_seleccionados = $('input:checkbox:not(:checked)').map(function() {
            return this.value;
        }).get();

        var projectID = $('#projectID').val();
        segmentsSave(seleccionados,no_seleccionados,projectID)
}

function segmentsSave(segmentos,no_seleccionados,project_id) {
    // Setup CSRF tokens and all that good stuff so we don't get hacked
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
        var ajaxData = {secciones: segmentos.toString(),noseleccionados:no_seleccionados.toString(), project_id: project_id.toString()};
        $.ajax({
            url: '/erp/api/sections_for_project_save/',
            data: ajaxData,
            type: 'get',
            success: function(data) {
                alert(data[0].mensaje);
            },
            error: function(data) {
                alert('error!! ' + data.status);
            }
        });

   /* });*/
}