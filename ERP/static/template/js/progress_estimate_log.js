// Note through the comments that:
//                  "pel" = "Progress Estimate Log".



/**
 * Function to receive the logs in json format and to process them to generate the table to be rendered.
 * @param json_log_files
 * @returns {string}
 */


function create_logs_table(json_logs) {
    var table_string = "<table class='table'>" +
        "<thead>" +
        "<tr>" +
        "<td>Id</td>" +
        "<td>Descripción</td>" +
        "<td>Fecha</td>" +
        "<td>Usuario</td>" +
        "<td>Acción</td>" +
        "</tr>" +
        "</thead>" +
        "" +
        "<tbody>";
    for (var count in json_logs) {
        table_string += "<tr class='pel_row' id='"+json_logs[count].id+"'>" +
            "<td>" + json_logs[count].id + "</td>" +
            "<td>" + json_logs[count].description + "</td>" +
            "<td>" + json_logs[count].date + "</td>" +
            "<td>" + json_logs[count].user_fullname + "</td>" +
            "<td>" +
            "<a href='/admin/ERP/progressestimatelog/" + json_logs[count].id + "/change/'>" +
            "Eliminar" +
            "</a>" +
            "</td>" +
            "</tr>";
    }

    table_string += "</tbody>" +
        "</table>";

    return table_string;

}



/**
 * Function to receive the log files in json format and to process them to generate the table to be rendered.
 * @param json_log_files
 * @returns {string}
 */
function create_log_files_table(json_log_files) {
    var table_string = "<table class='table'>" +
        "<thead>" +
        "<tr>" +
        "<td>Id</td>" +
        "<td>Archivo</td>" +
        "<td>Mime</td>" +
        "<td>Acción</td>" +
        "</tr>" +
        "</thead>" +
        "" +
        "<tbody>";
    for (var count in json_log_files) {
        table_string += "<tr>" +
            "<td>" + json_log_files[count].id + "</td>" +
            "<td>" + json_log_files[count].file + "</td>" +
            "<td>" + json_log_files[count].mime + "</td>" +
            "<td>" +
            "<a href='/admin/ERP/logfile/" + json_log_files[count].id + "/delete/'>" +
            "Eliminar" +
            "</a>" +
            "</td>" +
            "</tr>";
    }

    table_string += "</tbody>" +
        "</table>";


    return table_string;

}


function getInputByForm(formId) {
    values = {};
    $.each($('#' + formId).serializeArray(), function (i, field) {
        values[field.name] = field.value;

    });
    return values;
}


/**
 * To provide the needed interaction with the template.
 */
$(document).ready(function () {

    // Note: due to Django structure:
    //      1.) json_logs is defined in the template progress_estimate_log_form.html
    //      2.) json_log_files is defined in the template progress_estimate_log_form.html

    // To show the first found log.
    if (json_logs.length > 0) {
        logs_table = create_logs_table(json_logs);
        $("#logs-table").html(logs_table);
    }else{
        $("#logs-table").html("Aún no has cargado bitácoras de estimación");
    }


    // To show the files of the first 'pel' found in the data structure.
    if (json_log_files.length > 0) {
        files_table = create_log_files_table(json_log_files);
        $("#log-files-table").html(files_table);
    }else{
        $("#log-files-table").html("Aún no has cargado evidencias");
    }


    // Setting the value for the select.
    $("#id_progress_estimate_log").val(json_log_files[0].id);


    // Function run when click on pel table row
    $(document).on('click', '.pel_row', function () {
        var log_id = $(this).attr('id');

        // Setting the value for the hidden input in the file field at the pel_file form.
        $("#id_progress_estimate_log").val(log_id);


        // Ajax to retrieve the files assigned to a pel.

        var url = "/erp/api/log_files_for_progress_estimate_log";
        var data = {
            'pel_id': log_id
        };
        data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function (response) {
                json_log_files = response;
                console.log("Response: " + JSON.stringify(response));
                var to_render = "";
                if (response.length > 0) {
                    to_render = create_log_files_table(response);

                } else {
                    to_render = "<span>Aún no has cargado evidencias</span>";

                }

                $("#log-files-table").html(to_render);
            },
            dataType: "json"
        });
    });


    // Function run when the pel form is submitted.
    $("#pel-form").submit(function(){
        console.log("Submitting pel form");

        // Ajax to call the save pel endpoint.
        var url = "/erp/forms_api/save_pel_form";
        var data = getInputByForm("pel-form");
        data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function (response) {
                console.log("Got response: " + JSON.stringify(response));
                // Add the register to the table
                json_logs.push(response.saved_log);
                logs_table = create_logs_table(json_logs);
                $("#logs-table").html(logs_table);

                // Reset the form
                $("#pel-form")[0].reset();

            },
            error: function(error){
              alert(error.responseText)
            },
            dataType: "json"
        });

        return false;
    });


     // Function run when the pel form is submitted.
    $("#pel-file-form").submit(function(){
        console.log("Submitting pel form");

        // Ajax to call the save pel endpoint.
        var url = "/erp/forms_api/save_pel_file_form";
        var data = getInputByForm("pel-file-form");
        data['csrfmiddlewaretoken'] = $('[name=csrfmiddlewaretoken]').val();


        var formData = new FormData(this);
        formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {

                // Preserve the pel value.
                var pel_id = $("#id_progress_estimate_log").val();

                // Reset the form.
                $("#pel-file-form")[0].reset();

                // Reassign the value for the pel
                $("#id_progress_estimate_log").val(pel_id);


                json_log_files.push(response.file_obj);
                files_table = create_log_files_table(json_log_files);
                $("#log-files-table").html(files_table);




            }
        });

        return false;
    });

});
