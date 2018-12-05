$(document).ready(function () {
    var activado = 0;
    $('tr.add-row td a').click(function (){

        //location.href="#";
        //alert("activado pre if" + activado);
        if (activado==0) {
             // alert("activado post if" + activado);
            activado = 1;
            // alert("activado a 1" + activado);
            limite = $('#id_payment_plan').val();
            amount = $('#id_amount').val();

            //alert(limite);
            if (limite==1){
                limite = 12;
            }
            else{
                limite=14;
            }

            for (var i = 0; i < limite; i++) {
               // alert("i" + i);
                $link = $('tr.add-row td a');
                $link[0].click()
                amount_month = amount/limite;
                document.getElementById("id_employeeloandetail_set-"+i+"-amount").value=amount_month;
            }
        }
    });
});