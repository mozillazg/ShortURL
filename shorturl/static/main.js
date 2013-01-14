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


// 去除字符串首尾空白符（" dog ".trim() === "dog"）
// http://stackoverflow.com/questions/1418050/string-strip-for-javascript
if (typeof(String.prototype.trim) === "undefined") {
  String.prototype.trim = function() {
    return String(this).replace(/^\s+|\s+$/g, '');
  };
}

// 表单验证
function validForm() {
  if (!document.getElementById) return false;
  var url = document.getElementById("url").value.trim();
  var msg = document.getElementById("msg");
  if (!url) {
    document.getElementById("url").className = "warning";
    msg.innerHTML = "Can't be white-space chars!";
    msg.className = "visible";
    return false;
  } else {
    document.getElementById("url").className = "";
    document.getElementById("url").value = addScheme(url);
  }
  //msg.className = "hidden";
  msg.innerHTML = "";
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
// 处理用户输入的 URL（添加 URL scheme）
function addScheme(url) {
  var url = url;
  var hasScheme;
  // 支持的 URL 协议
  var scheme2 = /^[a-z][a-z0-9+.\-]*:\/\//i;
  var scheme3 = ['git@', 'mailto:', 'javascript:', 'about:', 'opera:',
                 'afp:', 'aim:', 'apt:', 'attachment:', 'bitcoin:',
                 'callto:', 'cid:', 'data:', 'dav:', 'dns:', 'fax:', 'feed:',
                 'gg:', 'go:', 'gtalk:', 'h323:', 'iax:', 'im:', 'itms:',
                 'jar:', 'magnet:', 'maps:', 'message:', 'mid:', 'msnim:',
                 'mvn:', 'news:', 'palm:', 'paparazzi:', 'platform:',
                 'pres:', 'proxy:', 'psyc:', 'query:', 'session:', 'sip:',
                 'sips:', 'skype:', 'sms:', 'spotify:', 'steam:', 'tel:',
                 'things:', 'urn:', 'uuid:', 'view-source:', 'ws:', 'xfire:',
                 'xmpp:', 'ymsgr:', 'doi:'];
  var url_lower = url.toLowerCase();
  var scheme = scheme2.test(url_lower);
  if (!scheme) {
    for (var i=0; i<scheme3.length; i++) {
      var url_splits = url_lower.split(scheme3[i]);
      if (url_splits.length > 1) {
        hasScheme = true;
        break;
      }
    }
    if (!hasScheme) {
      url = 'http://' + url;
    }
  }
  return url
}

// 处理服务器返回的 json 数据
function displayResult(request) {
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
    document.getElementById("shorten").value = shorten;
    //qrcode.alt = "QR Code for URL " + shorten;
    document.getElementById("result").style.visibility = "visible";
    document.getElementById("shorten").focus();
    document.getElementById("shorten").select();
    document.getElementById("submit").className = "pointer";
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
// ajax 提交 URL 数据，返回短网址信息
function postFormData() {
  var request = getHTTPObject();
  if (request) {
    var url = document.getElementById("url").value.trim();
    var data = "url=" + url;
    request.open("POST", "/j/shorten", true);
    request.onreadystatechange = function() {displayResult(request);};
    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    request.send(data);
    document.getElementById("submit").className = "progress";
    document.getElementById("result").style.visibility = "hidden";
  }
}


// 拦截 submit 事件，提交前验证数据并改用 ajax 发送数据
function submitEvent() {
  if (!document.getElementById) return false;
  if (!document.getElementById("submit")) return false;
  document.getElementById("submit").onclick = function () {
    if (validForm()) {
      postFormData();
    }
    return false;
  }
}

addLoadEvent(submitEvent);


// 当文本框获得焦点时，全选文本框内容
function selectAll() {
  if (!document.getElementsByTagName) return false;
  if (!document.getElementsByTagName("input")) return false;
  var textInputs = document.getElementsByTagName("input");
  for (var i=0; i<textInputs.length; i++) {
    var input = textInputs[i];
    if ((input.type == "text") || (input.type == "url")) {
      input.onclick = function() {
        this.select();
      };
    }
  }
}

addLoadEvent(selectAll);
