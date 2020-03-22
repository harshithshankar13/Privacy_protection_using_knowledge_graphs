var imported = document.createElement('script');
imported.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
document.head.appendChild(imported);

// run on tab update
chrome.tabs.onUpdated.addListener(sendURL);

function sendURL(tabId, changeInfo, tab){
    console.log(changeInfo.url);
    console.log(tabId);
    console.log(tab.url);
    // send url to server
    $.getJSON('http://127.0.0.1:5000/hello', {url:tab.url} ,function (data, textStatus, jqXHR){
      $('p').append(data.firstName);
  });
}