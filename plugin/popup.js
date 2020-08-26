// // global variables
// var privacyScoreGlo = 0
// var PSdetailsGlo = "Loading..."
// var privacyScoreSet = false
var websiteTypeGlo;
var websiteURLGlo;

$(document).ready(function () {
  chrome.browserAction.setBadgeText({ text: "" });
  // triples view ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  $("button.viewTriples").click(function () {
    $.ajax({
      type: "POST", url: 'http://localhost:5000/getRDF', success: function (response) {

        htmlcode = "<html><head><title> View Triples </title></head><body> <h1> Welcome to Linked Data application.</h1> <p> Triples represented below are the information about the companies whose website you have visited in the past.</p> <table border='1'>";
        htmlcode = htmlcode + "<tr> <th> Subject </th> <th> Predicate </th> <th> Object </th> </tr>"
        for (var i = 0; i < response['results']['bindings'].length; i++) {
          htmlcode = htmlcode + "<tr> <td>" + response['results']['bindings'][i]['s']['value'] + "</td><td>" + response['results']['bindings'][i]['p']['value'] + "</td><td>" + response['results']['bindings'][i]['o']['value'] + "</td></td>";
        }
        htmlcode = htmlcode + "</table></body></html>";
        var url = "data:text/html," + encodeURIComponent(htmlcode);
        chrome.tabs.create({ url: url });
      }
    });
  });
  //++++++++++++++++++++++++++++++++++++++++++++++++++++++

  // User profile ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  $("button.userProfile").click(function () {
    chrome.tabs.create({ 'url': chrome.extension.getURL('userProfile.html') });
     //chrome.storage.sync.clear(function(){  }); // to clear storage
  });
  //++++++++++++++++++++++++++++++++++++++++++++++++++++++

  // Linked login ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  $("button.LInkedInLogin").click(function () {
    // $.ajax({
    //   method: "GET",
    // headers: {
    //     'Access-Control-Allow-Credentials' : true,
    //     'Access-Control-Allow-Origin':'*',
    //     'Access-Control-Allow-Methods':'GET',
    //     'Access-Control-Allow-Headers':'application/json'
    // },
    // url: "https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77mpeeyrvnkjaa&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2FuserProfile&state=fooobar&scope=r_liteprofile%20r_emailaddress",
    // // data: { 
    // //   response_type: 'code',
    // //   client_id: '77mpeeyrvnkjaa', 
    // //   redirect_uri: 'http://localhost:5000/userProfile',
    // //   scope: 'r_emailaddress'},
    //   success: function(data) {
    //       document.getElementById("LILogIn").innerHTML = data
    //       // console.log(data)
    //       //chrome.tabs.create(data);
    //     }
    // });

    // //chrome.tabs.create({url:"http://localhost:5000/userProfile"});

    chrome.tabs.create({ url: 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=77mpeeyrvnkjaa&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2FuserProfile&state=fooobar&scope=r_liteprofile%20r_emailaddress' })
  });
  //++++++++++++++++++++++++++++++++++++++++++++++++++++++

  // privacyScore and details labels set++++++++++++++++++++++++++++++++++++++
  chrome.storage.sync.get(null, function (result) {
    console.log('Value currently is ' + JSON.stringify(result));
    privacyScoreGlo = result.privacyScoreGlo;
    PSdetailsGlo = result.PSdetailsGlo;
    privacyScoreSet = result.privacyScoreSet
    getWebUserCorrInfo = result.getWebUserCorrInfo
    websiteTypeGlo = result.websiteType
    websiteURLGlo = result.websiteMainURL

    console.log("privacyScoreSet: ", privacyScoreSet)
    console.log("getWebUserCorrInfo: ", getWebUserCorrInfo)

    if (privacyScoreSet === true) {
      document.getElementById("privacyScore").style.display = '';
      document.getElementById("PSdetails").style.display = '';
      document.getElementById("privacyScore").innerHTML = "Privacy risk score: " + privacyScoreGlo;
      document.getElementById("PSdetails").innerHTML = "Reason for privacy risk score: <br>" + PSdetailsGlo;
    }
    if (getWebUserCorrInfo === true) {
      document.getElementById("getWebsiteUserCorrelationDiv").innerHTML = "Do you use and trust this " + websiteTypeGlo + " type of website?";
      document.getElementById("getWebsiteUserCorrelationDiv").style.display = '';
      document.getElementById("getWebsiteUserCorrelationTextBox").style.display = '';
      document.getElementById("submitUsrInfo").style.display = '';
    }

  });
  //++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  // store user other information in local storage +++++++++++++++++++++++++++++
  $("button.submitUsrInfo").click(function () {
    var resFromWebsiteUserCorrelationTextBox = document.getElementById("getWebsiteUserCorrelationTextBox").value;
    console.log(resFromWebsiteUserCorrelationTextBox);
    if (resFromWebsiteUserCorrelationTextBox === "Yes") {

      // get Website User Correlation info
      chrome.storage.sync.get("Trusted_" + websiteTypeGlo,
        function (websiteURLs) {
          var websiteURLPersis = [];

          if (websiteURLs !== undefined && websiteURLs["Trusted_" + websiteTypeGlo] !== undefined){
            for (i = 0; i < websiteURLs["Trusted_" + websiteTypeGlo].length; i++) {
              websiteURLPersis.push(websiteURLs["Trusted_" + websiteTypeGlo][i]);
            }
          }
          
          console.log("websiteURLPersis before :", websiteURLPersis)
          // add websiteURL to old list
          websiteURLPersis.push(websiteURLGlo);

          console.log("websiteURLPersis :", websiteURLPersis)

          // store Website User Correlation info
          chrome.storage.sync.set({
            ["Trusted_" + websiteTypeGlo]: websiteURLPersis
          },
            function () {
              console.log('user and website\'s correlation is stored');
            });
        });


    }

    document.getElementById("getWebsiteUserCorrelationDiv").style.display = 'none';
    document.getElementById("getWebsiteUserCorrelationTextBox").style.display = 'none';
    document.getElementById("submitUsrInfo").style.display = 'none';
  });
  //++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

});

// get message from backgroud.js
chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse) {
    if (request.msg == "privacyScoreReason") {
      document.getElementById("privacyScore").style.display = '';
      document.getElementById("privacyScore").innerHTML = "Privacy risk score: " + request.data.privacyScore;
      document.getElementById("PSdetails").innerHTML = "Reason for privacy risk score: " + request.data.reason;
    }

    if (request.msg == "clearPrivacyScoreReason") {
      document.getElementById("privacyScore").innerHTML = "Loading...";
      document.getElementById("PSdetails").innerHTML = "Loading...";
    }

    if (request.msg == "getWebsiteUserCorrelation") {
      websiteTypeGlo = request.data.websiteType;
      websiteURLGlo = request.data.websiteMainURL
      document.getElementById("getWebsiteUserCorrelationDiv").innerHTML = "Is this your " + request.data.websiteType;
      document.getElementById("getWebsiteUserCorrelationDiv").style.display = '';
      document.getElementById("getWebsiteUserCorrelationTextBox").style.display = '';
      document.getElementById("submitUsrInfo").style.display = '';

    }
  }
);



