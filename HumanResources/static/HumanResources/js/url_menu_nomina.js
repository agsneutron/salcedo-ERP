$(function () {
    if (/payrollgroup/.test(window.location.href)) {
        $('#e2>a').addClass('active');
        $('#e2>a').removeClass('collapsed');
    }

});
$(function () {
    if (/payrollgroup\/+add/.test(window.location.href)) {
        $('#e2>a').addClass('active');
        $('#e2>a').removeClass('collapsed');
    }

});

$(function () {
    if (/payrollperiod/.test(window.location.href)) {
        $('#e1>a').addClass('active');
        $('#e1>a').removeClass('collapsed');
    }

});
$(function () {
    if (/payrollperiod\/+add/.test(window.location.href)) {
        $('#e1>a').addClass('active');
        $('#e1>a').removeClass('collapsed');
    }

});

$(function () {
    if (/payrolltype/.test(window.location.href)) {
        $('#e0>a').addClass('active');
        $('#e0>a').removeClass('collapsed');
    }

});
$(function () {
    if (/payrolltype\/+add/.test(window.location.href)) {
        $('#e0>a').addClass('active');
        $('#e0>a').removeClass('collapsed');
    }

});

$(function () {
    url = window.location.href.toString();
    if (/penalty=S/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }else{
        if (/tipo=2/.test(window.location.href)){
            $('#e4>a').addClass('active');
            $('#e4>a').removeClass('collapsed');
        }
        else {
            if (/earningsdeductions\/+add/.test(window.location.href)) {
                $('#e3>a').addClass('active');
                $('#e3>a').removeClass('collapsed');
            }
            else{
                if (/earningsdeductions/.test(window.location.href)) {
                    $('#e3>a').addClass('active');
                    $('#e3>a').removeClass('collapsed');
                }
            }
        }
    }

});
$(function () {
    if (/tipo=2/.test(window.location.href)){
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }
    else {
        if (/earningsdeductions\/+add/.test(window.location.href)) {
            alert("DyP-Add");
            $('#e3>a').addClass('active');
            $('#e3>a').removeClass('collapsed');
        }
    }
});

$(function () {
    if (/earningsdeductions\/+?penalty=S/.test(window.location.href)) {
        alert("Penalizaciones");
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }

});

$(function () {
    if (/uploadedemployeeassistancehistory/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');

       /*  $('#e3>a').removeClass('active');
 $('#e3>a').addClass('collapsed withripple');*/
    }

});
$(function () {
    if (/uploadedemployeeassistancehistory\/+add/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }

});

$(function () {
    if (/employeeloan/.test(window.location.href)) {
        $('#e5>a').addClass('active');
        $('#e5>a').removeClass('collapsed');
    }

});
$(function () {
    if (/employeeloan\/+add/.test(window.location.href)) {
        $('#e5>a').addClass('active');
        $('#e5>a').removeClass('collapsed');
    }

});

$(function () {
    if (/employeedropout/.test(window.location.href)) {
        $('#e6>a').addClass('active');
        $('#e6>a').removeClass('collapsed');
    }

});
$(function () {
    if (/employeedropout\/+add/.test(window.location.href)) {
        $('#e6>a').addClass('active');
        $('#e6>a').removeClass('collapsed');
    }

});



/*
$(function () {
    if (/\?+type=1/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }
});
*/

