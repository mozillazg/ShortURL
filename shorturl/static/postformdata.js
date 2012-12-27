function displayResult() {
  if ((request.readyState == 4) && request.status == 200) {
    var responseJson = JSON.parse(request.responseText);
    var shorten = responseJson.shorten;
    var qrcodeSrc = "http://qrcode101.duapp.com/qr?chl=" + shorten + "&chs=200x200&chld=M|0"
    document.getElementById("shorten").value = responseJson.shorten;
    document.getElementById("qrcode").src= qrcodeSrc;
    document.getElementById("result").className = "visible";
    document.getElementById("shorten").focus();
    //document.getElementById("shorten").select();
  }
}
function postFormData() {
  request = getHTTPObject();
  if (request) {
    var url = document.getElementById("long-url").value;
    var data = "url=" + url;
    request.open("POST", "/j/shorten", true);
    request.onreadystatechange = displayResult;
    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    request.send(data);
  }
}
function submitEvent() {
  document.getElementById("submit-data").onclick = function () {
    postFormData();
    return false;
  }
}
addLoadEvent(submitEvent);
