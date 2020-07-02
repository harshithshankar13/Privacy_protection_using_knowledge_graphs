$(document).ready(function(){
    $("button.LILogin").click(function(){
        $.getJSON('https://www.linkedin.com/oauth/v2/authorization',
        { response_type: 'code',
          client_id: '77mpeeyrvnkjaa', 
          redirect_uri: 'http://localhost:5000/userProfile',
          scope:r_liteprofile, r_emailaddress}, 
         function (data, textStatus, jqXHR){
            document.getElementById('LIStatus').innerHTML = data;
        });
    });
});