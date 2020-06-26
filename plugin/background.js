var imported = document.createElement('script');
imported.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
document.head.appendChild(imported);

// run on tab update
chrome.tabs.onUpdated.addListener(sendURL);

function sendURL(tabId, changeInfo, tab){
  var url = tab.url;
  console.log(url)
  if (url !== undefined && changeInfo.status == "complete" && url != "chrome://newtab/" ) {

  window.lat = 0; 
  window.longi = 0;
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position)
    {
      console.log(position.coords.latitude);
      lat = position.coords.latitude;
      console.log(position.coords.longitude);
      longi = position.coords.longitude;
      
        // send url to server
        $.getJSON('http://localhost:5000/privacyMetric', {url:tab.url, userLocationLat:lat, userLocationLong:longi}, function (data, textStatus, jqXHR){
        console.log(data)  ;
        $('p').append(data);
       });
      
    });
  
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }

  // // send url to server
  // $.getJSON('http://localhost:5000/privacyMetric', {url:tab.url, userLocation:{lat:lat, long:longi}} ,function (data, textStatus, jqXHR){
  //   $('p').append(data.firstName);
  // });
}
}