$(document).ready(function(){
    $('#submit').click(function(){
       const s_city= document.getElementById('s_city').value;
       const d_city= document.getElementById('d_city').value;

       $.ajax(
           {
               url: '',
               type:'get',
               data:{
                   's_city':s_city,
                   'd_city':d_city,
               },
               success: function (response){
                   $('#result').empty().append(response.result)
               }
           }
       )


    });
});