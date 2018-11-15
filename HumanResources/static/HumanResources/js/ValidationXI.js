/*Created by Xavi*/



$(payment_method).ready(function(){
    $("Deposito").on("change", function(){

        if ($("account_number").val() =="" && $("CLABE").val() =="" && $("bank").val() ==""){

    alert("No puedes dejar los campos: Número de Cuenta, Clave, Banco vacios");

        }
    });
});


$(payment_method).ready(function(){
    $("Transferencia Interbancaria").on("change", function(){

         if ($("account_number").val() =="" && $("CLABE").val() =="" && $("bank").val() ==""){

    alert("No puedes dejar los campos: Número de Cuenta, Clave, Banco vacios");

        }
    });
});