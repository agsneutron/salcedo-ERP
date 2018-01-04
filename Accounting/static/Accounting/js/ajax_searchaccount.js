/**
 * Created by Ari_ on 13/12/17.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', main);

function main() {
    $j('#searchaccount').on('click', search);
}

//http://127.0.0.1:8000/accounting/search_accounts?name=Cuenta%202&number=2&subsidiary_account_array=1&
// nature_account_array=2&grouping_code_array=2&level=2&item=2
function search() {
    var subsidiary_account_array = $j("#msSubsidiaryAccountArray").multiselect("getChecked").map(function () {
        return this.value;
    }).get();
    var nature_account_array = $j("#msNatureAccountArray").multiselect("getChecked").map(function () {
        return this.value;
    }).get();
    var grouping_code_array = $j("#msGroupingCodeArray").multiselect("getChecked").map(function () {
        return this.value;
    }).get();
    var account = $j("#account").val();
    var number = $j("#number").val();
    var level = $j("#level").val();
    var rubro = $j("#rubro").val();
    var internal_company = $j("#internal_company").val();
    var url = "/accounting/search_accounts?";

    if (account.toString() != "") {
        url = url + "&name=" + account.toString();
    }
    if (number.toString() != "") {
        url = url + "&number=" + number.toString();
    }
    if (subsidiary_account_array.toString() != "") {
        url = url + "&subsidiary_account_array=" + subsidiary_account_array.toString();
    }
    if (nature_account_array.toString() != "") {
        url = url + "&nature_account_array=" + nature_account_array.toString();
    }
    if (grouping_code_array.toString() != "") {
        url = url + "&grouping_code_array=" + grouping_code_array.toString();
    }
    if (level.toString() != "") {
        url = url + "&level=" + level.toString();
    }
    if (rubro.toString() != "") {
        url = url + "&rubro=" + rubro.toString();
    }
    if (internal_company.toString()!="") {
        url=url+"&internal_company="+internal_company.toString();
    }
    //alert(url);
    searchengine(url);
}


function searchengine(url) {
    // Setup CSRF tokens and all that good stuff so we don't get hacked
    $.ajaxSetup(
        {
            beforeSend: function (xhr, settings) {
                if (settings.type == "POST")
                    xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
                if (settings.type == "GET")
                    xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
            }
        }
    );

    // Get an Oauth2 access token and then do the ajax call, because SECURITY
    /*  $.get('/obras/register_by_token', function(ans) {
     var ajaxData = { access_token: ans.access_token};
     //alert(ans.access_token);*/
    var message = "";

    $.ajax({
        url: url,
        type: 'get',
        success: function (data) {
            //console.log(data);
            displayResults(data);

        },
        error: function (data) {

            /*alert('error!! ' + data.status);*/
            /* alert('Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error: ' + data.status);*/
            message = 'Ocurrió un error al realizar la búsqueda, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')

        }
    });


    /* });*/
}

function displayResults(data) {
    var sHtml = "";
    var sTable = "";

    $j('#divTable').html("<div></div>");
    sHtml = '<table class="table-filtros table table-striped table_s" cellspacing="0" width="100%" id="tablaResultados">'
        + ' <colgroup>'
        + ' <col width="15%">'
        + ' <col width="7%">'
        + ' <col width="14%">'
        + ' <col width="14%">'
        + ' <col width="14%">'
        + ' <col width="14%">'
        + ' <col width="29%">'
        + ' </colgroup>';

    sTable = '<thead>'
        + '<tr>'
        + '<th>Nombre</th>'
        + '<th>No.</th>'
        + '<th>Nivel</th>'
        + '<th>Rubro</th>'
        + '<th>Subcuenta</th>'
        + '<th>Naturaleza</th>'
        + '<th>Cód. Agrupador SAT</th>'
        + '</tr>'
        + '</thead>'
        + '<tbody>';

    for (var i = 0; i < data.length; i++) {
        sTable += '<tr>'
            + '<td class="result1 selectable">' + data[i].name + '</td>'
            + '<td class="result1 selectable">' + data[i].number + '</td>'
            + '<td class="result1 selectable">' + checkIfNone(data[i].level) + '</td>'
            + '<td class="result1 selectable">' + checkIfNone(data[i].item) + '</td>'
            + '<td class="result1 selectable">' + checkIfNone(data[i].subsidiary_account) + '</td>'
            + '<td class="result1 selectable">' + data[i].nature_account + '</td>'
            + '<td class="result1 selectable">' + data[i].grouping_code + '</td>'
            + '</tr>'
    }

    sTable += '</tbody>'
        + '</table>';

    sHtml += sTable;

    sScript = '<script id="js" type="text/javascript"  class="init">'
        + '$("#tablaResultados").DataTable( {'
        + 'destroy: true,';

    sTable = 'columnDefs: ['
        + '       {'
        + '           className: "mdl-data-table__cell--non-numeric"'
        + '       }'
        + '   ],'

        + '   responsive: true,'
        + '   "bInfo": false,';

    sScript += sTable;
    sScript += ' "pageLength": 6,';

    sTable = '   "bLengthChange": false,'
        + '   "language": {'
        + '       "sProcessing": "Procesando...",'
        + '       "sLengthMenu": "Mostrar _MENU_ registros",'
        + '       "sZeroRecords": "No se encontraron resultados",'
        + '       "sEmptyTable": "La consulta no generó resultados a mostrar",'
        + '       "sInfo": "",'
        + '       "sInfoEmpty": "",'
        + '       "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",'
        + '       "sInfoPostFix": "",'
        + '       "sSearch": "",'
        + '      "sUrl": "",'
        + '       "sInfoThousands": ",",'
        + '       "sLoadingRecords": "Cargando...",'
        + '       "oPaginate": {'
        + '           "sFirst": "Primero",'
        + '           "sLast": "Último",'
        + '          "sNext": ">",'
        + '           "sPrevious": "<"'
        + '}'
        + '},'
        + '} );'
        + '</script>';

    sScript += sTable;

    $j('#divTable').html(sHtml + sScript);

}


function checkIfNone(val) {
    if (val == 'undefined' || val == null || val == undefined) {
        return '-';
    }
    return val;
}