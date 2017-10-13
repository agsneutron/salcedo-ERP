/**
 * Created by bamaa on 14/09/17.
 */
$(document).on('ready', function () {
    /*
     Only do the cleanup if the field didn't contain a value already
     this is used for the edit form
     */
    $('#guardaSegmento').on('click', guardaSegmento);

});

function configura_segmentos(project_id) {

    $('#projectID').val(project_id);

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
    var ajaxData = {project_id: project_id.toString()};
    $.ajax({
        url: '/erp/api/sections_by_project/',
        data: ajaxData,
        type: 'get',
        success: function (data) {
            putSections(data);

        },
        error: function (data) {
            /*
             alert('Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error: ' + data.status);
             */
            var message = 'Ocurrió un error al configurar el proyecto, favor de informar al administrador del sistema el siguiente código de error:\n' + data.status;
            $('#alertModal').find('.modal-body p').text(message);
            $('#alertModal').modal('show')
        }
    });

}


function putSections(data) {
    var sHTML = "";
    var chk = true;
    var subchk = true;
    document.getElementById('accordion').innerHTML = '';
    for (var i = 0; i < data.length; i++) {
        //alert(data[i].project_section_id)
        //data[i].project_section_name
        if (data[i].project_section_status == "1") {
            chk = "checked";
        }
        else {
            chk = "";
        }

        sHTML = sHTML + '<div class="panel panel-default">';
        sHTML = sHTML + '<div class="panel-heading" role="tab" id="headingTwo">';
        sHTML = sHTML + '   <h4 class="panel-title ms-rotate-icon">';
        /*        sHTML = sHTML + '   <div class="togglebutton" style="position: relative">';
         sHTML = sHTML + '       <label class="switch-right">';
         //sHTML = sHTML + '           <input onchange="toggleCheckboxParent(this)" class = "parent-' + i + '" type="checkbox" name="checkSegment" id="'+ data[i].project_section_name+'" value="'+ data[i].project_section_id +'"  '  +chk+ '>';
         //sHTML = sHTML + '           <span class="toggle"></span>';
         sHTML = sHTML + '       </label>';
         sHTML = sHTML + '   </div>';*/
        sHTML = sHTML + '   <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapse' + data[i].project_section_id + '" aria-expanded="false" aria-controls="collapse' + data[i].project_section_id + '">';
        sHTML = sHTML + '       <i class="zmdi ">&nbsp;</i>' + data[i].project_section_name;
        sHTML = sHTML + '   </a>';
        sHTML = sHTML + '   </h4>';
        sHTML = sHTML + '</div>';
        sHTML = sHTML + '<div id="collapse' + data[i].project_section_id + '" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingOne">';
        sHTML = sHTML + '   <div class="panel-body">';
        //alert(sHTML);
        //alert(data[i].inner_sections.length);

        for (var j = 0; j < data[i].inner_sections.length; j++) {
            //alert(data[i].inner_sections[j].project_section_name);
            pss = data[i].inner_sections[j].project_section_status;
            if (pss == "1") {
                subchk = "checked";
            }
            else {
                subchk = "";
            }
            //data[i].inner_sections[j].project_section_status
            //alert(data[i].inner_sections[j].project_section_name);
            //data[i].inner_sections[j].project_section_id
            sHTML = sHTML + '       <div>';
            sHTML = sHTML + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + data[i].inner_sections[j].project_section_name;
            sHTML = sHTML + '           <div class="togglebutton" style="float: right">';
            sHTML = sHTML + '               <label>';
            sHTML = sHTML + '                   <input class = "child-' + i + '" type="checkbox" name="checkSegment" id="' + data[i].inner_sections[j].project_section_name + '" value="' + data[i].inner_sections[j].project_section_id + '" ' + subchk + '>';
            //onchange="toggleCheckboxChild(this)"
            sHTML = sHTML + '               <span class="toggle"></span>';
            sHTML = sHTML + '               </label>';
            sHTML = sHTML + '           </div>';
            sHTML = sHTML + '       </div>';
            sHTML = sHTML + '<hr class="divide-item">';
            //alert(sHTML);
        }
        sHTML = sHTML + '   </div>';
        sHTML = sHTML + '</div>';
        sHTML = sHTML + '</div>';
        sHTML = sHTML + '<div class="clearfix"></div>';


    }

    $('#accordion').append(sHTML);

}

function toggleCheckboxParent(element) {

    str = element.className.split("-");
    clasep = "parent-" + str[1];
    clasec = "child-" + str[1];
    var welParent = document.getElementsByClassName(clasep);
    var welChild = document.getElementsByClassName(clasec);

    welParent[0].checked = !welParent[0].checked;

    if (welParent[0].checked) {
        welParent[0].checked = false
    }
    else {
        welParent[0].checked = true;
    }
    for (var j = 0; j < welChild.length; j++) {
        if (welChild[j].checked) {
            welChild[j].checked = false
        }
        else {
            welChild[j].checked = true;
        }
    }
}

function toggleCheckboxChild(element) {

    str = element.className.split("-");
    clasep = "parent-" + str[1];
    clasec = "child-" + str[1];
    var welParent = document.getElementsByClassName(clasep);
    var welChild = document.getElementsByClassName(clasec);
    var status = false;

    element.checked = !element.checked;

    if (element.checked) {
        element.checked = false
    }
    else {
        element.checked = true;
    }
    for (var j = 0; j < welChild.length; j++) {
        if (welChild[j].checked) {
            status = true
        }
    }
    welParent[0].checked = status;
}


function checkBoxesByProject(data) {
    for (var i = 0; i < data.length; i++) {
        elemento = eval(data[i].project_section_name);
        if (parseInt(data[i].project_section_status) == 1) {
            elemento.checked = true;
        }
        else {
            elemento.checked = false;
        }
        for (var j = 0; j < data[i].inner_sections.length; j++) {
            elemento = eval(data[i].inner_sections[j].project_section_name);
            if (parseInt(data[i].inner_sections[j].project_section_status) == 1) {
                elemento.checked = true;
            }
            else {
                elemento.checked = false;
            }
        }

    }
}

function guardaSegmento() {
    var seleccionados = $('input:checkbox:checked').map(function () {
        return this.value;
    }).get();
    var no_seleccionados = $('input:checkbox:not(:checked)').map(function () {
        return this.value;
    }).get();

    var projectID = $('#projectID').val();
    segmentsSave(seleccionados, no_seleccionados, projectID)
}

function segmentsSave(segmentos, no_seleccionados, project_id) {
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
    var ajaxData = {
        secciones: segmentos.toString(),
        noseleccionados: no_seleccionados.toString(),
        project_id: project_id.toString()
    };
    $.ajax({
        url: '/erp/api/sections_for_project_save/',
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