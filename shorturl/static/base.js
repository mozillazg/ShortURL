// 用于更新 window.onload 事件
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

// 检测 XMLHttpRequest 对象是否可用
// 当可用时返回一个 XMLHttpRequest 对象
function getHTTPObject() {
  if (typeof XMLHttpRequest == "undefined") {
    XMLHttpRequest = function() {
      try { return new ActiveXObject("Msxml2.XMLHTTP.6.0");
      } catch (e) {}
      try { return new ActiveXObject("Msxml2.XMLHTTP.3.0");
      } catch (e) {}
      return false;
    }
  }
  return new XMLHttpRequest();
}


// 去除字符串首尾空白符（" dog ".trim() === "dog"）
// http://stackoverflow.com/questions/1418050/string-strip-for-javascript
if(typeof(String.prototype.trim) === "undefined")
{
    String.prototype.trim = function()
    {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}
// 表单验证
function validForm() {
  if (!document.getElementById) return false;
  var url = document.getElementById("url").value.trim();
  var msg = document.getElementById("msg")
  if (!url) {
    document.getElementById("url").className = "warning"
    msg.lastChild.nodeValue = "↑↑ Can't be whitespace chars! ↑↑";
    msg.className = "visible";
    return false;
  }
  msg.className = "hidden";
  return true;
}

// ajax 提交 URL 数据，返回短网址信息
function displayResult() {
  if (!document.getElementById) return false;
  if ((request.readyState == 4) && request.status == 200) {
    var responseJson = JSON.parse(request.responseText);
    var shorten = responseJson.shorten;
    var qrcodeSrc = "http://qrcode101.duapp.com/qr?chl=" + shorten + "&chs=200x200&chld=M|0"
    var qrcode = document.getElementById("qrcode");
    document.getElementById("shorten").value = shorten;
    qrcode.src= qrcodeSrc;
    qrcode.alt = "QR Code for URL " + shorten;
    document.getElementById("result").className = "visible";
    document.getElementById("shorten").focus();
    //document.getElementById("shorten").select();
    document.getElementById("submit").className = "pointer";
  }
}
function postFormData() {
  request = getHTTPObject();
  if (request) {
    var url = document.getElementById("url").value.trim();
    var data = "url=" + url;
    request.open("POST", "/j/shorten", true);
    request.onreadystatechange = displayResult;
    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    request.send(data);
    document.getElementById("submit").className = "progress";
  }
}
function submitEvent() {
  document.getElementById("submit").onclick = function () {
    if (validForm()) {
      postFormData();
    }
    return false;
  }
}
addLoadEvent(submitEvent);
