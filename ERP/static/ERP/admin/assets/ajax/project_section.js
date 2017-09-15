/**
 * Created by bamaa on 14/09/17.
 */

$(document).on('ready', function() {
    /*
     Only do the cleanup if the field didn't contain a value already
     this is used for the edit form
     */

    $('#guardaSegmento').on('click', guardaSegmento)

});


function  guardaSegmento() {
        var seleccionados = $('input:checkbox:checked').map(function() {
            return this.value;
        }).get();
        segmentsSave(seleccionados,1)
}

function segmentsSave(segmentos,project_id) {
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
        var ajaxData = {secciones: segmentos.toString(), project_id: project_id.toString()};
        $.ajax({
            url: '/erp/api/sections_for_project_save/',
            data: ajaxData,
            type: 'get',
            success: function(data) {
                alert(data);
            },
            error: function(data) {
                alert('error!! ' + data.status);
            }
        });

   /* });*/
}