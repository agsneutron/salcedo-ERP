/**
 * Created by ariaocho on 15/12/17.
 */


var $j = jQuery.noConflict();
var url = "";
var tar_url = "/humanresources/transactions_by_account_report?";

$j(document).on('ready', main);

function main(){
     $j('#searchtransactions').on('click', search);
}

/*  Parámetros:*

        fiscal_period_year = entero
        fiscal_period_month = entero
        type_policy_array = arreglo con los id’s
        lower_folio = entero
        upper_folio = entero
        lower_registry_date = date [m/d/YYYY]
        upper_registry_date = date [m/d/YYYY]
        description = String
        lower_account_number = entero
        upper_account_number = entero
        lower_debit = entero
        upper_debit = entero
        lower_credit = entero
        upper_credit = entero
        reference = string*/

function search() {
    var url_policieslist=""
    var fiscal_period_year = $j("#fiscal_period_year").val();
    var fiscal_period_month = $j("#fiscal_period_month").val();
    var employee_key = $j("#employee_key").val();
    var name = $j("#name").val();
    var rfc = $j("#rfc").val();

    var sta_url = "/humanresources/search_transactions_by_employee?";

    url="";

    if (fiscal_period_year.toString()!="") {
        url = url + "&fiscal_period_year=" + fiscal_period_year.toString();
    }

    if (fiscal_period_month.toString()!="") {
        url=url+"&fiscal_period_month="+fiscal_period_month.toString();
    }

    if (employee_key.toString()!="") {
        url=url+"&employee_key="+employee_key.toString();
    }
    if (name.toString()!="") {
        url=url+"&name="+name.toString();
    }
    if (rfc.toString()!="") {
        url=url+"&rfc="+rfc.toString();
    }


    url_policieslist = "lower_fiscal_period_year="+ fiscal_period_year.toString() +"&uppper_fiscal_period_year="+ fiscal_period_year.toString()  +"&lower_fiscal_period_month="+ fiscal_period_month.toString() +"&upper_fiscal_period_month="+ fiscal_period_month.toString() +"&account=";
    //alert(url);
    var staurl = sta_url+url;
    searchengine(staurl,url_policieslist);
}




function searchengine(staurl,url_policieslist) {
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
    var message="";

    $.ajax({
        url: staurl,
        type: 'get',
        success: function (data) {
            //console.log(data);
            displayResults(data,url_policieslist);

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

function displayResults(data,url_policieslist){
    var sHtml="";
    var sTable="";
    var sScript = "";


    $j('#divTable').html("<div></div>");
    sHtml ='<table class="table-filtros table table-striped table_s" cellspacing="0" width="100%" id="tablaResultados">'
            + ' <colgroup>'
                +' <col width="15%">'
                +' <col width="45%">'
                +' <col width="17%">'
                +' <col width="17%">'
                +' <col width="3%">'


                +' </colgroup>';

    sTable= '<thead>'
                        +'<tr>'
                            +'<th>Año Fiscal</th>'
                            +'<th>Mes Fiscal</th>'
                            +'<th>Nombre</th>'
                            +'<th>Clave Empleado</th>'
                            +'<th class="no-sorting">Exportar</th>'


                        +'</tr>'
                    +'</thead>'
                    +'<tbody>';

    //<a data-toggle="modal" data-target="#myModal" href="'+ tarurl + url + '&account='+data.accounts[i].account_number+'" class="btn btn-raised btn-default btn-xs">'
    //        + '<i class="fa fa-file-excel-o color-default eliminar" style="color: green;"></i></a>'

    for (var i = 0; i < data.accounts.length; i++) {
            sTable += '<tr>'
            + '<td class="result1 selectable">'+ data.accounts[i].payroll_period_year +  '</td>'
            + '<td class="result1 selectable">'+ data.accounts[i].payroll_period_month + '</td>'
            + '<td class="result1 selectable">'+ data.accounts[i].payroll_period_name + '</td>'
            + '<td class="result1 selectable">'+ data.accounts[i].employee_key + '</td>'
            + '<td class="result1 selectable"><a href="'+ tar_url + url + '&employee_key='+data.accounts[i].employee_key+'" class="btn btn-raised btn-default btn-xs">'
            + '<i class="fa fa-file-excel-o color-default eliminar" style="color: green;"></i></a>' + '</td>'
            + '</tr>'
    }
    sTable +='</tbody>'
          +'</table>';

    sHtml +=sTable;

    sScript='<script id="js" type="text/javascript"  class="init">'
	        +'$("#tablaResultados").DataTable( {'
            + 'destroy: true,';

    sTable ='columnDefs: ['
             +'       {'
             +'           className: "mdl-data-table__cell--non-numeric"'
             +'       }'
             +'   ],'

             +'   responsive: true,'
             +'   "bInfo": false,';

    sScript += sTable;
    sScript +=' "pageLength": 6,';

    sTable = '   "bLengthChange": false,'
             +'   "language": {'
             +'       "sProcessing": "Procesando...",'
             +'       "sLengthMenu": "Mostrar _MENU_ registros",'
             +'       "sZeroRecords": "No se encontraron resultados",'
             +'       "sEmptyTable": "La consulta no generó resultados a mostrar",'
             +'       "sInfo": "",'
             +'       "sInfoEmpty": "",'
             +'       "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",'
             +'       "sInfoPostFix": "",'
             +'       "sSearch": "",'
             +'      "sUrl": "",'
             +'       "sInfoThousands": ",",'
             +'       "sLoadingRecords": "Cargando...",'
             +'       "oPaginate": {'
             +'           "sFirst": "Primero",'
             +'           "sLast": "Último",'
             +'          "sNext": ">",'
             +'           "sPrevious": "<"'
          +'}'
          +'},'
	      +'} );'
          +'</script>';

    sScript += sTable;

    $j('#divTable').html(sHtml+sScript);

}