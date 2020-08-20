var script = document.createElement('script');
script.setAttribute("type", "text/javascript")
script.textContent = `
function onScriptAdd() {
var inputEle = document.getElementsByTagName("INPUT");
for (i = 0; i < inputEle.length; i++) {
  console.log("sendTODOC");
  inputEle[i].addEventListener("focusout", sendToDoc, false);
}

function sendToDoc() {
  // data to send
  var data = {
    changedInputTextKey: this.value
  };
  
  // send data through a DOM event
  document.dispatchEvent(new CustomEvent('sendToDoc', {detail: data}));
};
};

onScriptAdd();`;


(document.head || document.documentElement).appendChild(script); 
console.log("Script added!");
script.remove();

// Listen you CRX event
document.addEventListener('sendToDoc', function (event) {
  var data = event.detail;

  // domain visited
  domain = new URL(location.href).host;

  // send reason for privacyScore to popup.js
  chrome.runtime.sendMessage({
    msg: "getUserEnteredInfo",
    data: data,
    domain: domain
  });
});

