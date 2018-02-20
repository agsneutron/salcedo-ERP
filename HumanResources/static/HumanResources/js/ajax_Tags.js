/**
 * Created by bamaa on 26/09/17.
 */
/**
 * Created by bamaa on 20/02/18.
 */

var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

var datosJson
var newToken


function main_consulta() {
    $j.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                //xhr.overrideMimeType( "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8" );
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                //xhr.overrideMimeType( "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8" );
			}
		}
	});

    callGetTags();


}

function callGetTags(){
    //$j.get("/obras/register_by_token", function(respu) {

        $j.ajax({
            url: '/humanresources/api/get_tags',
            type: 'get',
            success: function(data) {
                datosJson=data;
                populateTags(data);

            },
            error: function(data) {
            var message = 'Ocurrió un error, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show');
            }
        });
    //});

}

//llenar el multiselect de Tags
function populateTags(data){
    //clearField('#tags');

    //fill with Productos
    var sHtml = '<select id="mstags" name="tags" class="selectpicker" data-style="select-with-transition" title="Etiquetas" multiple data-size="7">';
    for (var i = 0; i < data.length; i++) {
        sHtml = sHtml + '<option value=' + data[i].id + '>' + data[i].nombre + '</option>';
    }
    sHtml = sHtml + '</select>';

    $j('#divTags').html(sHtml);

}

//limpiar el multiselect field antes de cargar las nuevas opciones
function clearField(field){
    // Clean the field

    $j(field).html('');
    //$j(field).multiselect('destroy');
}
//obtener el parametro de la URL
function $_GET(param)
{
    /* Obtener la url completa */
    url = document.URL;
    /* Buscar a partir del signo de interrogación ? */
    url = String(url.match(/\?+.+/));
    /* limpiar la cadena quitándole el signo ? */
    url = url.replace("?", "");
    /* Crear un array con parametro=valor */
    url = url.split("&");

    /*
    Recorrer el array url
    obtener el valor y dividirlo en dos partes a través del signo =
    0 = parametro
    1 = valor
    Si el parámetro existe devolver su valor
    */
    x = 0;
    while (x < url.length)
    {
        p = url[x].split("=");
        if (p[0] == param)
        {
            return decodeURIComponent(p[1]);
        }
        x++;
    }
}