var imported = document.createElement('script');
imported.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
document.head.appendChild(imported);

// run on tab update
chrome.tabs.onUpdated.addListener(sendURL);

function sendURL(tabId, changeInfo, tab){
 // chrome.storage

 // domain visited
 domain = new URL(tab.url).host  ;
 console.log("Domain:", domain) ;
 
 // chrome history ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  var days = 90
  var startTimeInMicrosec = 1000 * 60 * 60 * 24 * days;
  var domainVisitCount = 0;
  chrome.history.search({text: '', startTime : (new Date).getTime() - startTimeInMicrosec, maxResults: 100}, function(data) {
    data.forEach(function(page) {
        if(new URL(page.url).host == domain)
        {
          domainVisitCount = domainVisitCount + page.visitCount ;
        }
    });
  });

  console.log("domainVisitCount: ",domainVisitCount );

  //++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
        // (@@LinkedIN logIn page) $.getJSON('https://www.linkedin.com/oauth/v2/authorization', 
        $.getJSON('http://localhost:5000/privacyMetric',
        {url:tab.url, userLocationLat:lat, userLocationLong:longi, domainVisitCount:domainVisitCount}, 
        function (data, textStatus, jqXHR){
        console.log(data.privacyScore) ;
        if(data.privacyScore > 0.5)
        {
          chrome.browserAction.setIcon({
            path: 'pp_red.png',
            //tabId: sender.tab.id
          });
        }
        else if (data.privacyScore > 0.2)
        {
          chrome.browserAction.setIcon({
          path: 'pp_yellow.png',
          //tabId: sender.tab.id
        });
        }
        else{
          chrome.browserAction.setIcon({
            path: 'pp_green.png',
            //tabId: sender.tab.id
          });
        }
        $('p').append(data);
       });
    });
  
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
    }
  }

  //++++++++++++++++++++++++++++++++++++++++++++++++++++++

  
  // send url to server - @ redundent
  // $.getJSON('http://localhost:5000/privacyMetric', {url:tab.url, userLocation:{lat:lat, long:longi}} ,function (data, textStatus, jqXHR){
  //   $('p').append(data.firstName);
  // });

}