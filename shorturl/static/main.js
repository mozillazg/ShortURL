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
    document.getElementById("url").value = url;
  }
  //msg.className = "hidden";
  msg.innerHTML = "";
  return true;
}

// 处理服务器返回的 json 数据
function displayResult(request) {
  if (!document.getElementById) return false;
  if ((request.readyState == 4) && request.status == 200) {
    var responseJson = JSON.parse(request.responseText);
    var shorten = responseJson.url;
    var qrcodeImage = '<img src="' + responseJson.qrcode + '" />';
    var result = document.getElementById("result");
    var qrcode = document.getElementById("qrcode");
    if (!qrcode) {
      qrcode = document.createElement('div');
      qrcode.id = "qrcode";
      qrcode.innerHTML = qrcodeImage;
      result.appendChild(qrcode);
    }
    else {
      qrcode.innerHTML = qrcodeImage;
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
    var csrft_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    var data = JSON.stringify({
      long_url: url,
      qrcode: true
    });
    request.open("POST", "/", true);
    request.setRequestHeader ("X-CSRFToken", csrft_token);
    request.setRequestHeader ("X-Requested-With", "XMLHttpRequest");
    request.onreadystatechange = function() {displayResult(request);};
    request.setRequestHeader("Content-Type", "application/json; charset=utf-8");
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
