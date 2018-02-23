/**
 * Created by ariaocho on 13/12/17.
 */
/**
 * Created by Ari_ on 13/12/17.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', main);

function main() {
    $j('#searchaccount').on('click', search);
    $j('#excelexport').on('click', export_excel);
    search();
}

//http://127.0.0.1:8000/accounting/search_commercial_allies?
//   name=nombre&rfc=12345678&email=test@test.com&phone_number=123456789&accounting_account_number=5&
//   bank_account=123456789&register_date_lower=12/12/2017&register_date_upper=12/14/2017&type=PROVIDER

function search() {
    perform_search(false);
}

function export_excel() {
    perform_search(true);
}


function perform_search(excel_export) {

    var name = $j("#name").val();
    var rfc = $j("#rfc").val();
    var email = $j("#email").val();
    var phone_number = $j("#phone_number").val();
    var accounting_account_number = $j("#accounting_account_number").val();
    var bank_account = $j("#bank_account").val();
    var register_date_lower = $j("#register_date_lower").val();
    var register_date_upper = $j("#register_date_upper").val();
    var type = $j("#type").val();
    var url = "/accounting/search_commercial_allies?";
    var services = $j("#services").val();

    if (name.toString() != "") {
        url = url + "name=" + name.toString() + "&";
    }
    if (rfc.toString() != "") {
        url = url + "rfc=" + rfc.toString() + "&";
    }
    if (email.toString() != "") {
        url = url + "email=" + email.toString() + "&";
    }
    if (phone_number.toString() != "") {
        url = url + "phone_number=" + phone_number.toString() + "&";
    }
    if (accounting_account_number.toString() != "") {
        url = url + "accounting_account_number=" + accounting_account_number.toString() + "&";
    }
    if (bank_account.toString() != "") {
        url = url + "bank_account=" + bank_account.toString() + "&";
    }
    if (register_date_lower.toString() != "") {
        url = url + "register_date_lower=" + register_date_lower.toString() + "&";
    }
    if (register_date_upper.toString() != "") {
        url = url + "register_date_upper=" + register_date_upper.toString() + "&";
    }

    if (services.toString() != "") {
        url = url + "services=" + services.toString() + "&";
    }

    if (excel_export) {
        url = url + "export_excel=1" + "&";
    }


    if (type.toString() != "") {
        url = url + "type=" + type.toString();

        if (excel_export) {
            window.location.replace(url)
        } else {
            searchengine(url, type)
        }
    }
    else {
        console.log("No TYPE");
    }
}


function searchengine(url, type) {
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
            displayResults(data, type);

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

function displayResults(data, type) {
    var sHtml = "";
    var sTable = "";

    $j('#divTable').html("<div></div>");
    sHtml = '<table class="table-filtros table" cellspacing="0" width="100%" id="tablaResultados">'
        + ' <colgroup>'
        + ' <col width="">'
        + ' <col width="">'
        + ' <col width="">'
        + ' <col width="">'
        + ' <col width="">'
        //+' <col width="5%">'
        + ' <col width="5%">'
        + ' <col width="5%">'
        + ' <col width="5%">'
        + ' </colgroup>';

    sTable = '<thead>'
        + '<tr>'
        + '<th>Nombre</th>'
        + '<th>RFC</th>'
        + '<th>E-mail</th>'
        + '<th>Cuenta Contable</th>'
        + '<th>Banco</th>'
        // +'<th>Registro</th>'
        + '<th class="no-sorting">Ver</th>'
        + '<th class="no-sorting">Editar</th>'
        + '<th class="no-sorting">Eliminar</th>'

        + '</tr>'
        + '</thead>'
        + '<tbody>';

    for (var i = 0; i < data.length; i++) {
        var type_id = ""
        if (type == "PROVIDER") {
            type_id = 0
        }
        else if (type == "CREDITOR") {
            type_id = 1
        }
        else if (type == "THIRD_PARTY") {
            type_id = 2
        }

        sTable += '<tr>'
            + '<td class="result1 selectable">' + data[i].name + '</td>'
            + '<td class="result1 selectable">' + data[i].rfc + '</td>'
            + '<td class="result1 selectable">' + data[i].email + '</td>'
            + '<td class="result1 selectable">' + data[i].accounting_account + '</td>'
            + '<td class="result1 selectable">' + data[i].bank_account_name + '</td>'
            //+ '<td class="result1 selectable">'+ data[i].register_date + '</td>'
            + '<td class="text-center" style="width: 3%"><a '
            + 'href="/admin/Accounting/commercialally/' + data[i].id + '" '
            + 'class="btn btn-raised btn-default btn-xs"><i '
            + 'class="fa fa-eye color-default eliminar"></i></a></td> '
            + '<td class="text-center" style="width: 3%"><a '
            + 'href="/admin/Accounting/commercialally/' + data[i].id + '/change/?type=' + type_id + '"'
            + 'class="btn btn-raised btn-default btn-xs"><i '
            + 'class="fa fa-pencil color-default eliminar"></i></a></td> '
            + '<td class="text-center" style="width: 3%"><a '
            + 'href="/admin/Accounting/commercialally/' + data[i].id + '/delete" '
            + 'class="btn btn-raised btn-default btn-xs"><i '
            + 'class="fa fa-trash-o color-danger eliminar"></i></a> '
            + '</tr>'
    }

    sTable += '</tbody>'
        + '</table>';

    sHtml += sTable;

    sScript = '<script id="js" type="text/javascript"  class="init">'
        + '$("#tablaResultados").DataTable( {'


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
        + ''

        + '</script>';

    sScript += sTable;

    $j('#divTable').html(sHtml + sScript);

}