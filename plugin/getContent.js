var inputEle = document.getElementsByTagName("INPUT");
console.log("sendTODOC")
for (i = 0; i < inputEle.length; i++) {
  inputEle[i].setAttribute("onfocusout", "sendToDoc(this)");
}

var script = document.createElement('script');
script.setAttribute("type", "text/javascript")
script.textContent = `function sendToDoc(sentObject) {
 
  // data to send
  var data = {
    changedInputTextKey: sentObject.value
  };
  
  // send data through a DOM event
  document.dispatchEvent(new CustomEvent('sendToDoc', {detail: data}));
}`;


(document.head).appendChild(script); //||document.documentElement
console.log("Script added!");
script.remove();

// Listen you CRX event
document.addEventListener('sendToDoc', function (event) {
  var data = event.detail;
  
  // domain visited
  domain = new URL(location.href).host;
  console.log("data1212: ", domain)

  // send reason for privacyScore to popup.js
  chrome.runtime.sendMessage({
    msg: "getUserEnteredInfo",
    data: data,
    domain: domain
  });
});

