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
    msg.lastChild.nodeValue = "↑↑ Valid URL! ↑↑";
    msg.className = "visible";
    return false;
  }
  msg.className = "hidden";
  return true;
}
// 生成 QR Code
function create_qrcode(text) {//, typeNumber, errorCorrectLevel) {
  var qr = new QRCode(4, QRErrorCorrectLevel.H);
  var html;
  qr.addData(text);
  qr.make();
  html = '<table id="qrcode-table">';
  for (var r = 0; r < qr.getModuleCount(); r++) {
    html +="<tr>";
    for (var c = 0; c < qr.getModuleCount(); c++) {
      if (qr.isDark(r, c) ) {
        html += '<td class="dark" />';
      } else {
        html += '<td class="white" />';
      }
    }
    html += "</tr>";
  }
  html += "</table>";
  return html;
}

// ajax 提交 URL 数据，返回短网址信息
function displayResult() {
  if (!document.getElementById) return false;
  if (!JSON) {
    JSON = {};
    JSON.parse = function (json) {
      return eval("(" + json + ")");
    };
  }
  if ((request.readyState == 4) && request.status == 200) {
    var responseJson = JSON.parse(request.responseText);
    var shorten = responseJson.shorten;
    //var qrcodeSrc = "http://qrcode101.duapp.com/qr?chl=" + shorten + "&chs=200x200&chld=M|0"
    var result = document.getElementById("result");
    var qrcode = document.getElementById("qrcode");
    var qrcodeTable = create_qrcode(shorten);
    if (!qrcode) {
      qrcode = document.createElement('div');
      qrcode.id = "qrcode";
      qrcode.innerHTML = qrcodeTable;
      result.appendChild(qrcode);
    }
    else {
      qrcode.innerHTML = qrcodeTable;
    }
    //var qrcode = document.getElementById("qrcode");
    document.getElementById("shorten").value = shorten;
    //qrcode.src= qrcodeSrc;
    //qrcode.alt = "QR Code for URL " + shorten;
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
