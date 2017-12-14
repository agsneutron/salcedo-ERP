/**
 * Created by Ari_ on 13/12/17.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', search);

//http://127.0.0.1:8000/accounting/search_accounts?name=Cuenta%202&number=2&subsidiary_account_array=1&
// nature_account_array=2&grouping_code_array=2&level=2&item=2
    $j('#searchaccount').on('click', search());
function search() {
    var subsidiary_account_array = $j("#msSubsidiaryAccountArray").multiselect("getChecked").map(function(){return this.value;}).get();
    var nature_account_array = $j("#msNatureAccountArray").multiselect("getChecked").map(function(){return this.value;}).get();
    var grouping_code_array = $j("#msGroupingCodeArray").multiselect("getChecked").map(function(){return this.value;}).get();
    var account = $j("#account").val();
    var number = $j("#number").val();
    var level = $j("#level").val();
    var rubro = $j("#rubro").val();
    var url = "/accounting/search_accounts?";
    if (account.toString() != "") {
        url = url + "&name=" + account.toString();
    }
    if (number.toString() != "") {
        url=url+"&number="+number.toString();
    }
    if (subsidiary_account_array.toString() != "") {
        url=url+"&subsidiary_account_array="+subsidiary_account_array.toString();
    }
    if (nature_account_array.toString() != "") {
        url=url+"&nature_account_array="+nature_account_array.toString();
    }
    if (grouping_code_array.toString() != "") {
        url=url+"&grouping_code_array="+grouping_code_array.toString();
    }
    if (level.toString() != "") {
        url=url+"&level="+level.toString();
    }
    if (rubro.toString() != "") {
        url=url+"&rubro="+rubro.toString();
    }
    alert(url);
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
            alert(data);

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