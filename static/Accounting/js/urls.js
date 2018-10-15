$(function () {
    if (/searchthird/.test(window.location.href)) {
        $('#e5>a').addClass('active');
        $('#e5>a').removeClass('collapsed');
    }

});

$(function () {
    if (/\?+type=2/.test(window.location.href)) {
        $('#e5>a').addClass('active');
        $('#e5>a').removeClass('collapsed');
    }
});


$(function () {
    if (/searchaccount/.test(window.location.href)) {
        $('#e1>a').removeClass('collapsed');
        $('#e1>a').addClass('active');
    }
});

$(function () {
    if (/account\/+add/.test(window.location.href)) {
        $('#e1>a').removeClass('collapsed');
        $('#e1>a').addClass('active');
    }
});
$(function () {
    if (/\?+type=0/.test(window.location.href)) {
        $('#e3>a').addClass('active');
        $('#e3>a').removeClass('collapsed');
    }
});

$(function () {
    if (/searchprovider/.test(window.location.href)) {
        $('#e3>a').addClass('active');
        $('#e3>a').removeClass('collapsed');
    }
});

$(function () {
    if (/\?+type=1/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }
});

$(function () {
    if (/searchcreditors/.test(window.location.href)) {
        $('#e4>a').addClass('active');
        $('#e4>a').removeClass('collapsed');
    }
});

$(function () {
    if (/fiscalperiod\/+add/.test(window.location.href)) {
        $('#e7>a').addClass('active');
        $('#e7>a').removeClass('collapsed');
    }
});
$(function () {
    if (/fiscalperiod/.test(window.location.href)) {
        $('#e7>a').addClass('active');
        $('#e7>a').removeClass('collapsed');
    }
});

$(function () {
    if (/typepolicy\/+add/.test(window.location.href)) {
        $('#e8>a').addClass('active');
        $('#e8>a').removeClass('collapsed');
    }
});
$(function () {
    if (/typepolicy/.test(window.location.href)) {
        $('#e8>a').addClass('active');
        $('#e8>a').removeClass('collapsed');
    }
});

$(function () {
    if (/bank\/+add/.test(window.location.href)) {
        $('#e9>a').addClass('active');
        $('#e9>a').removeClass('collapsed');
    }
});
$(function () {
    if (/bank/.test(window.location.href)) {
        $('#e9>a').addClass('active');
        $('#e9>a').removeClass('collapsed');
    }
});

$(function () {
    if (/searchtransactions/.test(window.location.href)) {
        $('#e10>a').addClass('active');
        $('#e10>a').removeClass('collapsed');
    }
});

$(function () {
    if (/generategeneralbalance/.test(window.location.href)) {
        $('#e10>a').addClass('active');
        $('#e10>a').removeClass('collapsed');
    }
});
$(function () {
    if (/generatetrialbalance/.test(window.location.href)) {
        $('#e10>a').addClass('active');
        $('#e10>a').removeClass('collapsed');
    }
});