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
    console.log("geoLocation")
    window.lat = 0;
    window.longi = 0;
    if (navigator.geolocation) {

      navigator.geolocation.getCurrentPosition(function (position) {
        console.log(position.coords.latitude);
        lat = position.coords.latitude;
        console.log(position.coords.longitude);
        longi = position.coords.longitude;

        // send msg to content.js to get user data
        // chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        //   chrome.tabs.sendMessage(tabs[0].id, {msg: "setAttributes"}, function(response) {
        //     console.log("Nice");
        //   });
        // });

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

            // store privacyScore
            chrome.storage.sync.set({
              "privacyScoreGlo": data.privacyRiskScore,
              "PSdetailsGlo": data.reasonForPrivacyScore,
              "privacyScoreSet": true
            },
              function () {
                console.log('privacyScore is stored');
              });

            // get websiteType
            websiteType = data.websiteType
            if (websiteType != "privacyProtection") {
              console.log("websiteType", websiteType)
              var numberOfvisitToWebsiteType = 0;
              var userHistoryWebsiteTypes;

              userProfile = JSON.parse(userProfile);
              console.log("userProfile", typeof (userProfile));
              if (userProfile.hasOwnProperty("userHistoryWebsiteTypes")) {

                if (userProfile["userHistoryWebsiteTypes"].hasOwnProperty(String(websiteType))) {
                  console.log("Take 1");
                  userHistoryWebsiteTypes = userProfile["userHistoryWebsiteTypes"]
                  userHistoryWebsiteTypes[websiteType] = userProfile["userHistoryWebsiteTypes"][websiteType] + 1
                } else {
                  console.log("Take 2");
                  userHistoryWebsiteTypes = userProfile["userHistoryWebsiteTypes"]
                  console.log(userHistoryWebsiteTypes)
                  userHistoryWebsiteTypes[websiteType] = 1
                }
                // store userHistoryWebsiteTypes
                chrome.storage.sync.set({
                  "userHistoryWebsiteTypes": userHistoryWebsiteTypes
                },
                  function () {
                    console.log('userHistoryWebsiteTypes is stored');
                  });
              }
              else {
                console.log("Take 3");
                // store userHistoryWebsiteTypes
                chrome.storage.sync.set({
                  "userHistoryWebsiteTypes": { [websiteType]: 1 }
                },
                  function () {
                    console.log('userHistoryWebsiteTypes is stored');
                  });
              }

              console.log("userHistoryWebsiteTypes: ", userHistoryWebsiteTypes);


              //++++++++++++++++++++++++++++++++++++++++++++++++++++++
              // check if this website is present in the local userProfile
              var domainIsPresent = false
              // get Website User Correlation info
              chrome.storage.sync.get(["Trusted_" + websiteType],
                function (websiteURLs) {
                  console.log("websiteURLs: ", websiteURLs);
                  if (websiteURLs["Trusted_" + websiteType] != null) {
                    if (websiteURLs["Trusted_" + websiteType].includes(domain)) {
                      domainIsPresent = true;
                      chrome.storage.sync.set({
                        "getWebUserCorrInfo": false
                      },
                        function () {
                          console.log('GetWebUserCorrInfo is stored');
                        });
                    }
                  }

                  console.log("domainIsPresent: ", domainIsPresent)
                  // send msg to popup.js to get infomation 
                  if (tab.url != 'chrome-extension://bhjdkijlaepjnjnookngmcppbhdoahgh/popup.html' && tabIdLocal != tabId && domainIsPresent == false) {
                    console.log("tabId", tabId)

                    // display text on the icon
                    chrome.browserAction.setBadgeText({ text: "!!!" });

                    // send message to popup.js to get info about website correlation with user +++++++
                    chrome.runtime.sendMessage({
                      msg: "getWebsiteUserCorrelation",
                      data: {
                        "websiteType": websiteType,
                        "websiteMainURL": domain
                      }
                    });

                    chrome.storage.sync.set({
                      "getWebUserCorrInfo": true,
                      "websiteType": websiteType,
                      "websiteMainURL": domain
                    },
                      function () {
                        console.log('GetWebUserCorrInfo is stored');
                      });

                    tabIdLocal = tabId;
                  }


                });
            }
            // ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


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

// get data entered and calculate distance++++++++++++++++++++++++++++++++++++++++++
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  var userProfileValue = [];
  var userProfileKey = [];
  if (request.msg == "getUserEnteredInfo") {

    // compare data entered with userProfile

    chrome.storage.sync.get(null, function (result) {

      for (var key in result) {
        console.log("result: ", typeof (result[key]));
        if (result.hasOwnProperty(key)) {
          if (typeof (result[key]) != 'object') {
            userProfileValue.push(result[key]);
            userProfileKey.push(key);
          }
          else {
            if (Array.isArray(result[key])) {
              console.log("Array: ", result[key]);
              for (i = 0; i < result[key].length; i++) {
                if (typeof (result[key][i]) == "object") {
                  console.log("object: ", result[key]);
                  for (i = 0; i < Object.keys(result[key]).length; i++) {
                    for (j = 0; j < Object.keys(result[key][i]).length; j++) {
                      userProfileValue.push(Object.values(result[key][i])[j]);
                      userProfileKey.push(Object.keys(result[key][i])[j]);
                    }
                  }
                }
                else {
                  console.log("Array 1: ", result[key]);
                  userProfileValue.push(result[key][i]);
                  userProfileKey.push(key);
                }
              }
            }
            else {
              console.log("not an Array");
              for (i = 0; i < Object.keys(result[key]).length; i++) {
                userProfileValue.push(Object.values(result[key])[i]);
                userProfileKey.push(key);
              }
            }
          }
        }
      }

      // string match +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      console.log("changedInputTextKey: ", request.data.changedInputTextKey);
      console.log("userProfileValue: ", userProfileValue);
      var distance = {}
      for (i = 0; i < userProfileValue.length; i++) {
        if (typeof (userProfileValue[i]) == "string" && typeof (request.data.changedInputTextKey) == "string") {
          distance[userProfileKey[i]] = damerau_levenshtein_distance(userProfileValue[i], request.data.changedInputTextKey);
          
        }
      }
      console.log("damerau_levenshtein_distance: ", distance);
    });
    console.log(request.domain);
  }
});
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

// string matching+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
function damerau_levenshtein_distance(str1, str2) {
  var matx = []; //2d matrix

  // initialise
  var n = str1.length;
  var m = str2.length;

  if (n == 0) return m;
  if (m == 0) return n;

  //Create an matrix in javascript
  for (var i = n; i >= 0; i--) matx[i] = [];

  // assign values to 1st row and 1st column
  for (var i = n; i >= 0; i--) matx[i][0] = i;
  for (var j = m; j >= 0; j--) matx[0][j] = j;

  // calculate minimum steps required
  for (var i = 1; i <= n; i++) {
    var str1_i = str1.charAt(i - 1);

    // Step 4
    for (var j = 1; j <= m; j++) {

      //Check the total so far
      if (i == j && matx[i][j] > 4) return n;

      var str2_j = str2.charAt(j - 1);
      var cost = (str1_i == str2_j) ? 0 : 1; // Step 5

      //Calculate the minimum
      var a = matx[i - 1][j] + 1;
      var b = matx[i][j - 1] + 1;
      var c = matx[i - 1][j - 1] + cost;

      if (b < a) a = b;
      if (c < a) a = c;

      matx[i][j] = a;

      //Damerau transposition
      if (i > 1 && j > 1 && str1_i == str2.charAt(j - 2) && str1.charAt(i - 2) == str2_j) {
        matx[i][j] = Math.min(matx[i][j], matx[i - 2][j - 2] + cost);
      }
    }
  }

  // return total step required
  return matx[n][m];
}