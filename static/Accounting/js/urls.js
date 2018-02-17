$(function() {
  var loc = window.location.href; // returns the full URL
  if(/technology/.test(loc)) {
    $('#main').addClass('tech');
  }
});