var imported = document.createElement('script');
imported.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
document.head.appendChild(imported);

var tabIdLocal;

// run on tab update
chrome.tabs.onUpdated.addListener(sendURL);

// run on new tab @@todo - not activated yet
chrome.tabs.onCreated.addListener(setDefault);

function sendURL(tabId, changeInfo, tab) {

  // skip unwanted urls
  if (tab.url == "chrome://newtab/") {
    // clear previous datas privacyScore
    chrome.storage.sync.set({
      "privacyScoreGlo": 0,
      "PSdetailsGlo": "loading",
      "privacyScoreSet": false,
      "getWebUserCorrInfo": false
    },
      function () {
        console.log('clear previous datas is stored');
      });

    return true;
  }

  // domain visited
  domain = new URL(tab.url).host;
  console.log("Domain:", domain);

  // chrome history ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  var days = 90
  var startTimeInMicrosec = 1000 * 60 * 60 * 24 * days;
  var domainVisitCount = 0;
  chrome.history.search({ text: '', startTime: (new Date).getTime() - startTimeInMicrosec }, function (data) {
    data.forEach(function (page) {
      if (new URL(page.url).host == domain) {
        domainVisitCount = domainVisitCount + page.visitCount;
        console.log("domainVisitCount: ", domainVisitCount);
      }
    });
  });

  // get user profile from local storage +++++++++++++++++++++++++++++++++++++++++++++++++++++++
  // get user profile/graph from local browser storage  
  var userProfile;
  chrome.storage.sync.get(null, function (result) {
    console.log('Value currently is ' + JSON.stringify(result));
    userProfile = JSON.stringify(result);
  });

  //++++++++++++++++++++++++++++++++++++++++++++++++++++++
  var url = tab.url;
  console.log(url)
  if (url !== undefined && changeInfo.status == "complete" && url != "chrome://newtab/") {

    window.lat = 0;
    window.longi = 0;
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (position) {
        console.log(position.coords.latitude);
        lat = position.coords.latitude;
        console.log(position.coords.longitude);
        longi = position.coords.longitude;

        // send url to server
        // (@@LinkedIN logIn page) $.getJSON('https://www.linkedin.com/oauth/v2/authorization', 
        $.post('http://localhost:5000/privacyMetric',
          { url: tab.url, userProfile: userProfile, userLocationLat: lat, userLocationLong: longi, domainVisitCount: domainVisitCount },
          function (data, textStatus, jqXHR) {
            var privacyRiskScore = String(data.privacyRiskScore);

            console.log("privacyRiskScore", privacyRiskScore)

            // change icon based on privacy score
            if (data.privacyRiskScore > 0.5) {
              chrome.browserAction.setIcon({
                path: 'assets/pp_red.png'
                //tabId: sender.tab.id
              });

              // display text on the icon
              chrome.browserAction.setBadgeText({ text: privacyRiskScore });
              chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 0, 255] });

            }
            else if (data.privacyRiskScore > 0.2) {
              chrome.browserAction.setIcon({
                path: 'assets/pp_yellow.png'
                //tabId: sender.tab.id
              });
              // display text on the icon
              chrome.browserAction.setBadgeText({ text: privacyRiskScore });
              chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 0, 255] });
            }
            else {
              chrome.browserAction.setIcon({
                path: 'assets/pp_green.png'
                //tabId: sender.tab.id
              });
              //   // display text on the icon
              chrome.browserAction.setBadgeText({ text: privacyRiskScore });
              chrome.browserAction.setBadgeBackgroundColor({ color: [0, 0, 0, 255] });
            }

            // send reason for privacyScore to popup.js
            chrome.runtime.sendMessage({
              msg: "privacyScoreReason",
              data: {
                privacyScore: data.privacyRiskScore,
                reason: data.reasonForPrivacyScore
              }
            });

            // get websiteType
            websiteType = data.websiteType
            console.log("websiteType", websiteType)
            var numberOfvisitToWebsiteType = 0;
            var userHistoryWebsiteTypes;

            userProfile = JSON.parse(userProfile);
            console.log("userProfile", typeof (userProfile));
            if (userProfile.hasOwnProperty("userHistoryWebsiteTypes")) {
              if (userProfile["userHistoryWebsiteTypes"].hasOwnProperty(String(websiteType))) {
                userHistoryWebsiteTypes = userProfile["userHistoryWebsiteTypes"]
                userHistoryWebsiteTypes[websiteType] = userProfile["userHistoryWebsiteTypes"][websiteType] + 1
              } else {
                userHistoryWebsiteTypes = userProfile["userHistoryWebsiteTypes"]
                userHistoryWebsiteTypes[websiteType] = 1
              }
            }
            else {
              userHistoryWebsiteTypes = userProfile["userHistoryWebsiteTypes"]
              userHistoryWebsiteTypes[websiteType] = 1
            }

            console.log("userHistoryWebsiteTypes: ", userHistoryWebsiteTypes);
            
            //++++++++++++++++++++++++++++++++++++++++++++++++++++++
            if (tab.url != 'chrome-extension://bhjdkijlaepjnjnookngmcppbhdoahgh/popup.html' && tabIdLocal != tabId) {
              console.log("tabId", tabId)

              // display text on the icon
              chrome.browserAction.setBadgeText({ text: "!!!" });

              // send message to popup.js to get info about website correlation with user +++++++
              chrome.runtime.sendMessage({
                msg: "getWebsiteUserCorrelation",
                data: {
                  "websiteType": websiteType,
                  "websiteMainURL" : domain
                }
              });

              chrome.storage.sync.set({
                "getWebUserCorrInfo": true,
                "websiteType": websiteType,
                "websiteMainURL" : domain
              },
                function () {
                  console.log('GetWebUserCorrInfo is stored');
                });

              tabIdLocal = tabId;
            }
            // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            // store privacyScore
            chrome.storage.sync.set({
              "privacyScoreGlo": data.privacyRiskScore,
              "PSdetailsGlo": data.reasonForPrivacyScore,
              "privacyScoreSet": true,
              "userHistoryWebsiteTypes": userHistoryWebsiteTypes
            },
              function () {
                console.log('privacyScore is stored');
              });
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

// set default status of privacyScore and reasons @@todo - not activated yet
function setDefault(tabId, changeInfo, tab) {
  // restore default status and icon
  chrome.browserAction.setIcon({
    path: 'assets/pp.png'
  });

  // send reason for privacyScore to popup.js
  chrome.runtime.sendMessage({
    msg: "clearPrivacyScoreReason"
  });

  chrome.browserAction.setBadgeText({ text: "" });

  // clear previous datas privacyScore
  chrome.storage.sync.set({
    "privacyScoreGlo": 0,
    "PSdetailsGlo": "loading",
    "privacyScoreSet": false,
    "getWebUserCorrInfo": false
  },
    function () {
      console.log('privacyScore is stored');
    });
}