/**
 * Created by ariaocho on 14/12/17.
 */

var $j = jQuery.noConflict();

$j(document).on('ready', main);

function main(){
     $j('#searchpolicy').on('click', search);
}

/*  Parámetros:*

        lower_fiscal_period_year (int)
        upper_fiscal_period_year (int)

        lower_fiscal_period_month (int)[1 - 12]
        upper_fiscal_period_month (int)[1 - 12]

        type_policy_array (int) [arreglo id’s de los tipos de póliza]

        lower_folio (int)
        upper_folio (int)

        lower_registry_date (string) [m/d/YYYY]
        upper_registry_date (string) [m/d/YYYY]

        description (string)

        lower_account_number (int)
        upper_account_number (int)

        lower_debit (int)
        upper_debit (int)

        lower_credit (int)
        upper_credit (int)

        reference (string)*/

function search() {
    var lower_fiscal_period_year = $j("#lower_fiscal_period_year").val();
    var upper_fiscal_period_year = $j("#upper_fiscal_period_year").val();
    var lower_fiscal_period_month = $j("#lower_fiscal_period_month").val();
    var upper_fiscal_period_month = $j("#upper_fiscal_period_month").val();
    var type_policy_array = $j("#msTypePolicyArray").multiselect("getChecked").map(function(){return this.value;}).get();
    var lower_folio = $j("#lower_folio").val();
    var upper_folio = $j("#upper_folio").val();
    var lower_registry_date = $j("#lower_registry_date").val();
    var upper_registry_date = $j("#upper_registry_date").val();
    var description = $j("#description").val();
    var lower_account_number = $j("#lower_account_number").val();
    var upper_account_number = $j("#upper_account_number").val();
    var lower_debit = $j("#lower_debit").val();
    var upper_debit = $j("#upper_debit").val();
    var lower_credit = $j("#lower_credit").val();
    var upper_credit = $j("#upper_credit").val();
    var reference = $j("#reference").val();

    var url = "/accounting/search_policies?";

    if (lower_fiscal_period_year.toString()!="") {
        url = url + "&lower_fiscal_period_year=" + lower_fiscal_period_year.toString();
    }
    if (upper_fiscal_period_year.toString()!="") {
        url=url+"&upper_fiscal_period_year="+upper_fiscal_period_year.toString();
    }
    if (lower_fiscal_period_month.toString()!="") {
        url=url+"&lower_fiscal_period_month="+lower_fiscal_period_month.toString();
    }
    if (upper_fiscal_period_month.toString()!="") {
        url=url+"&upper_fiscal_period_month="+upper_fiscal_period_month.toString();
    }
    if (type_policy_array.toString()!="") {
        url=url+"&type_policy_array="+type_policy_array.toString();
    }
    if (lower_folio.toString()!="") {
        url=url+"&lower_folio="+lower_folio.toString();
    }
    if (upper_folio.toString()!="") {
        url=url+"&upper_folio="+upper_folio.toString();
    }
    if (lower_registry_date.toString()!="") {
        url=url+"&lower_registry_date="+lower_registry_date.toString();
    }
    if (upper_registry_date.toString()!="") {
        url=url+"&upper_registry_date="+upper_registry_date.toString();
    }
    if (description.toString()!="") {
        url=url+"&description="+description.toString();
    }
    if (lower_account_number.toString()!="") {
        url=url+"&lower_account_number="+lower_account_number.toString();
    }
    if (upper_account_number.toString()!="") {
        url=url+"&upper_account_number="+upper_account_number.toString();
    }
    if (lower_debit.toString()!="") {
        url=url+"&lower_debit="+lower_debit.toString();
    }
    if (upper_debit.toString()!="") {
        url=url+"&upper_debit="+upper_debit.toString();
    }
    if (lower_credit.toString()!="") {
        url=url+"&lower_credit="+lower_credit.toString();
    }
    if (upper_credit.toString()!="") {
        url=url+"&upper_credit="+upper_credit.toString();
    }
    if (reference.toString()!="") {
        url=url+"&reference="+reference.toString();
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
    var message="";

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

function displayResults(data){
    var sHtml="";
    var sTable="";

    $j('#divTable').html("<div></div>");
    sHtml ='<table class="table-filtros table table-striped table_s" cellspacing="0" width="100%" id="tablaResultados">'
            + ' <colgroup>'
                +' <col width="15%">'
                +' <col width="7%">'
                +' <col width="14%">'
                +' <col width="14%">'
                +' <col width="14%">'
                +' <col width="14%">'
                +' <col width="29%">'
                +' </colgroup>';

    sTable= '<thead>'
                        +'<tr>'
                            +'<th>Periodo Fiscal</th>'
                            +'<th>Póliza Tipo</th>'
                            +'<th>Folio</th>'
                            +'<th>Registro</th>'
                            +'<th>Descripción</th>'
                            +'<th>Referencia</th>'

                        +'</tr>'
                    +'</thead>'
                    +'<tbody>';

    for (var i = 0; i < data.length; i++) {
            sTable += '<tr>'
            + '<td class="result1 selectable">'+ data[i].fiscal_period_month + '-' + data[i].fiscal_period_year + '</td>'
            + '<td class="result1 selectable">'+ data[i].type_policy + '</td>'
            + '<td class="result1 selectable">'+ data[i].folio + '</td>'
            + '<td class="result1 selectable">'+ data[i].registry_date + '</td>'
            + '<td class="result1 selectable">'+ data[i].description + '</td>'
            + '<td class="result1 selectable">'+ data[i].reference + '</td>'
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