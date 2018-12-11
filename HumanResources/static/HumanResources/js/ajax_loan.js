$(document).ready(function () {
    var activado = 0;
    $('tr.add-row td a').click(function (){

        if (activado==0) {

            activado = 1;
            limite = $('#id_payment_plan').val();
            amount = $('#id_amount').val();

        if (amount==0) {

                window.alert('Falta llenar los campos: Empleado, Cantidad o Fecha');
                  //alert("Vriable " + amount + " amount");
                location.reload();

        }else{

            if (limite==1){
                limite = 12;
            }
            else{
                limite=14;
            }

            for (var i = 0; i < limite; i++) {
                $link = $('tr.add-row td a');
                $link[0].click()
                amount_month = amount/limite;
                document.getElementById("id_employeeloandetail_set-"+i+"-amount").value=amount_month;
            }

          }//Validacion del if else

        }
    });
});