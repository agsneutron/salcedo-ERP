/**
 * Created by bamaa on 25/08/17.
 */

var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

var newToken;
var datos = new Object();

function main_consulta() {

	getDataProjectList();
    /*$j("select#id_alineacion").on("change",function(){
    var projectId = $('select#project_list').find('option:selected').val();
            clearControl(id_eje);
            clearControl(id_tema);
            getDataEje(parseInt(projectId));

    });

    $j("select#id_eje").on("change",function(){
    var ejeId = $('select#id_eje').find('option:selected').val();
        if (ejeId == '') {
            clearControl(id_tema);
        }
        else(getDataPrograma(parseInt(ejeId)));

    });*/

}

function getDataProjectList(onSuccess) {
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

        $.ajax({
            url: '/erp/api/project_list/',
            type: 'get',
            success: function(data) {
                setProjectList(data);
            },
            error: function(data) {
                var message = 'Ocurrió un error al generar la lista de proyectos, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')
            }
        });

   /* });*/
}

// Once we're done filtering, we just put the results where they belong
function setProjectList(data){
    clearControl(project_list);
    for (var i = 0; i < data.length; i++) {
        $j("select#project_list").append(
            '<option value="'+data[i].id+'">' +
            data[i].key + " - " + data[i].nombreProyecto +
            '</option>'
        );
    }

}

function clearControl(idcontrol) {

    switch(idcontrol) {
    case project_list:
        $j('select#project_list')
        .empty()
        .append('<option value>  Seleccione... </option>');
        break;
    case id_eje:
        $j('select#id_eje')
        .empty()
        .append('<option value>  Seleccione... </option>');
        break;
    case id_tema:
        $j('select#id_tema')
        .empty()
        .append('<option value>  Seleccione... </option>');
        break;
    default:
        console.log("undefined_control");
    }
}
