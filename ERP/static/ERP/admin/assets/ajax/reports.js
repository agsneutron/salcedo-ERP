/**
 * Created by bamaa on 14/09/17.
 */
$(document).on('ready', function() {
    /*
     Only do the cleanup if the field didn't contain a value already
     this is used for the edit form
     */
    get_Projects();
    $('#get_report').on('click',Get_Financial_Report);

});

function get_Projects(){

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
            url: '/erp/api/project_list',
            type: 'get',
            success: function(data) {
                set_Projects(data);

            },
            error: function(data) {
                alert('error!! ' + data.status);
            }
        });

}

function set_Projects(data){
    clearControl("project_id");
    for (var i = 0; i < data.length; i++) {
        $("select#project_id").append(
            '<option value="'+data[i].id+'">' +
            data[i].nombreProyecto +
            '</option>'
        );
    }
}


function clearControl(idcontrol) {
    
    $('select#'+idcontrol)
        .empty()
        .append('<option value>  Seleccione... </option>');
    
}


function Get_Financial_Report(){
    var project_id = $('select#project_id').find('option:selected').val();
    var detail_level = $('select#detail_level').find('option:selected').val();
    if (parseInt(project_id) !=0 && detail_level.toString()!= "" ) {
        location.href="/reporting/get_financial_report?project_id=" + parseInt(project_id) + "&detail_level=" + detail_level.toString();
    }
}