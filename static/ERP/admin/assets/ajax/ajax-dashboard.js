/**
 * Created by ariaocho on 09/08/17.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

var newToken;
var datos = new Object();

function main_consulta() {
   // SetProjectData();

}

function GetProjectData(project_id,onSuccess) {
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
   /* $.get('/obras/register_by_token', function(ans) {
        var ajaxData = { access_token: ans.access_token};
        //alert(ans.access_token);*/
         var ajaxData = { project:project_id };

        $.ajax({
            url: 'api/get_project_info',
            type: 'get',
            data: ajaxData,
            success: function(data) {
                alert(data);
                setProjectData(data);
            },
            error: function(data) {
                var message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')
            }
        });

    }

// Once we're done filtering, we just put the results where they belong
function setProjectData(data){
    
}

