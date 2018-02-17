$(function () {
    if (/searchthird/.test(window.location.href)) {
        $('#e4>a').removeClass('collapsed');
        $('#e4>a').addClass('active');
    }
});

$(function () {
    if (/searchcreditors/.test(window.location.href)) {
        $('#e4>a').removeClass('collapsed');
        $('#e4>a').addClass('active');
    }
});

$(function () {
    if (/account/.test(window.location.href)) {
        $('#e1>a').removeClass('collapsed');
        $('#e1>a').addClass('active');
    }
});

$(function () {
    if (/searchprovider/.test(window.location.href)) {
        $('#e3>a').removeClass('collapsed');
        $('#e3>a').addClass('active');
    }
});

