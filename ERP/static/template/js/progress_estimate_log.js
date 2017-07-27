// Note through the comments that:
//                  "pel" = "Progress Estimate Log".


/**
 * Function to receive the log files in json format and to process them to generate the table to be rendered.
 * @param json_log_files
 * @returns {string}
 */
function create_log_files_table(json_log_files) {
    var table_string = "<table>" +
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


/**
 * To provide the needed interaction with the template.
 */
$(document).ready(function () {

    // Note: due to Django structure:
    //      1.) json_log_files is defined in the template progress_estimate_log_form.html

    // To show the files of the first 'pel' found in the data structure.
    if (json_log_files.length > 0) {
        files_table = create_log_files_table(json_log_files);
        $("#log-files-table").html(files_table);
    }


    // Setting the value for the select.
    $("#id_progress_estimate_log").val(json_log_files[0].id);


    // Function run when click on pel table row
    $(".pel_row").click(function () {

        var log_id = $(this).attr('id');
        // Setting the value for the select.
        $("#id_progress_estimate_log").val(log_id);


        // Ajax to retrieve the files assigned to a pel.

        var url = "/erp/api/log_files_for_progress_estimate_log";
        var data = {
            'pel_id': log_id
        };
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function (response) {
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
        var data = {
        };

        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function (response) {
                console.log("Got response: " + JSON.stringify(response));
            },
            error: function(error){
              console.log("Error: " + JSON.stringify(error));
            },
            dataType: "json"
        });

        return false;
    });

});
