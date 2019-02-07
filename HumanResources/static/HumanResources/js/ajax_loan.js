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

            for (var i = 0; i < limite -1; i++ ) {
               // alert("i" + i);
                $link = $('tr.add-row td a');
                $link[0].click()
                amount_month = amount/limite;
                amount_month = round(amount_month,2);
                dif_amount =  amount_month * limite;
                if (amount != dif_amount && i==0){
                    amount_month = amount_month + (amount-dif_amount);
                    amount_month = round(amount_month,2);
                }
                document.getElementById("id_employeeloandetail_set-"+i+"-amount").value=amount_month;
                document.getElementById("id_employeeloandetail_set-"+i+"-pay_number").value = i+1;
                $("#id_employeeloandetail_set-"+i+"-pay_number").addClass("no_change");

                if (i==limite-2){
                    j = limite-1;
                    document.getElementById("id_employeeloandetail_set-"+j+"-amount").value=amount_month;
                    document.getElementById("id_employeeloandetail_set-"+j+"-pay_number").value = j+1;
                    $("#id_employeeloandetail_set-"+j+"-pay_number").addClass("no_change");

                }

            }

          }//Validacion del if else

        }
    });


    function round(value, decimals) {
        return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
    }
});