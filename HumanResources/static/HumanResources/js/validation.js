$(document).ready(function () {

  $("input[name='rfc']").change(function (){

    rfc= $("input[name='rfc']").val();

    cve=  $("input[name='employee_key']").val();


    if(rfc!=cve) {
       alert("El RFC no coincide con la Clave RFC, asegurate de que coincidan ambos campos de RFC");
        $("input[name='rfc']").val(cve);
    }


   });


    $("input[name='employee_key']").change(function (){

       cve= $("input[name='employee_key']").val();

      $("input[name='rfc']").val(cve);

   });

});