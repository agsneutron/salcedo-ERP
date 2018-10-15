/**
 * Created by bamaa on 14/09/17.
 */


function sendSelected(url) {
    var seleccionados = $('input:checkbox:checked').map(function () {
        return this.value;
    }).get();

    url = url + "&employeesSelected=" + seleccionados.toString();
    location.href = url;
}

function callAssistanceValidate() {
    var path = window.location.pathname
    var arreglo_id = path.substr(56).split('/');
    var id_numero = arreglo_id[0];


    //$.get("/obras/register_by_token", function(respu) {
    var URL = "/admin/HumanResources/employeeassistance/incidences_by_period/" + id_numero + "/";

    location.href = URL
    //});

}


function callSave(seleccionados, payrollperiod) {
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
    var ajaxData = {
        payroll_period: payrollperiod.toString(),
        employeesSelected: seleccionados.toString(),
    };
    $.ajax({
        url: '/humanresources/api/generate_payroll_receipt',
        data: ajaxData,
        type: 'get',
        dataType: "html",
        success: function (data) {
            //alert(data[0].mensaje);
            message = 'Se guardó correctamente la configuración';
            $('#alertModalSuccess').find('.modal-body p').text(message);
            $('#alertModalSuccess').modal('show')
        },
        error: function (data) {

            /*alert('error!! ' + data.status);*/
            /* alert('Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error: ' + data.status);*/
            message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')

        }
    });

    /* });*/
}


/// Exclusion functionality
$(document).ready(function () {
    $('.employee_exclusion_checkbox').change(function () {
        $('#save_changes_button_label').html('Guardar Cambios');
        var button = $('#save_changes_button');
        if (button.css('display') == 'none') {
            button.fadeToggle(100);
        }
    });


});


function saveExcluded(payrollPeriod) {
    $('#save_changes_button_label').html('Guardando...');
    // Array containing employees and whether or not they are excluded
    var data = $(".employee_exclusion_checkbox").map(function () {
        return {"employee": this.value, "excluded": this.checked};
    }).get();

    callSaveExcludedEmployeesForPeriod(data, payrollPeriod);
}


function callSaveExcludedEmployeesForPeriod(data, payrollperiod) {
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
    var ajaxData = {
        payroll_period_id: payrollperiod,
        data: JSON.stringify(data),
    };
    $.ajax({
        url: '/humanresources/api/save_excluded_employees_for_period',
        data: ajaxData,
        type: 'get',
        dataType: "html",
        success: function (data) {
            $('#save_changes_button_label').html('Cambios Guardados');
        },
        error: function (data) {
            /*alert('error!! ' + data.status);*/
            /* alert('Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error: ' + data.status);*/
            message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')

        }
    });

    /* });*/
}