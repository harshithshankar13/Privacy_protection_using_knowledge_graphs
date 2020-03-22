/*var button = document.getElementById("get-url");

button.addEventListener("click", function(e){
  e.preventDefault();
  console.log("yes")

  const req = new XMLHttpRequest();
  const baseUrl = "http://127.0.0.1:5000/hello";
  //const baseUrl = "https://www.google.com/"
  //const urlParams = `email=${email}&password=${pwd}`;

  req.open("GET", baseUrl, true);
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  req.send("yes");

  req.onreadystatechange = function() { // Call a function when the state changes.
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
          console.log("Got response 200!");
      }
  }
});
*/

$(document).ready(function(){
  //$("button").click(function(){
    /*$.ajax({
      type: 'GET',
      cache: false,
      url: 'http://127.0.0.1:5000/hello',
      dataType: "json",
      success: function(data){
        console.log(data);
      }
    });*/
    var url_g
    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
      url_g = tabs[0].url;
  });
  
  console.log(url_g)
  console.log("aasda")
  
  $.getJSON('http://127.0.0.1:5000/hello', {url:url_g} ,function (data, textStatus, jqXHR){
      $('p').append(data.firstName);
  });

//   $.ajax({
//     url: 'http://127.0.0.1:5000/hello',
//     data: url_g,
//     type: 'POST',
//     success: function(response) {
//         console.log(response);
//     },
//     error: function(error) {
//         console.log(error);
//     }
// });
});