$(document).ready(function(){
  $("button.viewTriples").click(function(){
    $.ajax({type: "POST",url: 'http://localhost:5000/getRDF', success: function(response){

      htmlcode = "<html><head><title> View Triples </title></head><body> <h1> Welcome to Linked Data application.</h1> <p> Triples represented below are the information about the companies whose website you have visited in the past.</p> <table border='1'>" ;
      htmlcode = htmlcode + "<tr> <th> Subject </th> <th> Predicate </th> <th> Object </th> </tr>"
      for (var i = 0; i < response['results']['bindings'].length; i++) {
        htmlcode = htmlcode +"<tr> <td>" + response['results']['bindings'][i]['s']['value'] +"</td><td>"+ response['results']['bindings'][i]['p']['value'] +"</td><td>"+ response['results']['bindings'][i]['o']['value'] + "</td></td>";
      }
      htmlcode = htmlcode + "</table></body></html>" ;
      var url = "data:text/html," + encodeURIComponent(htmlcode);
      chrome.tabs.create({url: url});
    }});
  });

  // $("button.location").click(function() {
  //   if (navigator.geolocation) {
  //     navigator.geolocation.getCurrentPosition(showPosition);
  //     print(position.coords.latitude);
  //     print(position.coords.longitude);
  //   } else { 
  //     x.innerHTML = "Geolocation is not supported by this browser.";
  //   }
  // });
});


