var sdkName = document.getElementsByName("sdk_name")[0];
var packageName = document.getElementsByName("package_name")[0];
var proxyUrl = document.getElementsByName("proxy_url")[0];
var chnId = document.getElementsByName("chn_id")[0];
var sdkId = document.getElementsByName("sdk_id")[0];
var statusObj = document.getElementsByName("status")[0];
var enable_register = document.getElementsByName("enable_register")[0];
var enable_pay = document.getElementsByName("enable_pay")[0];

var gameShorName = window.location.host.split(".")[0];
var prefixUrl = "http://fxcb.umipay.com/";
var urls = {
    "10019" : "opay_iap",
    "10024" : "owpay_iap",
    "10025" : "owpay_iap",
};
var sdkNames = {
    "10019" : "iapopay",
    "10024" : "owpay_iap",
    "10025" : "h5",
};
var packageNames = {
    "10019" : "xxx.iapopay",
    "10024" : "xxx.ow",
    "10025" : "xxx.h5",
};
var appKeys = {
    "sghj" : "b780142b09f59a04",
    "jdwx" : "8b1c0b73738d40b7",
    "xyl" : "5b4c87a34471065f",
    "dyly" : "",
};
var serverSecrets = {
    "sghj" : "71207e5bda1f8d1d",
    "jdwx" : "69da2a872ce86982",
    "xyl" : "ff8396b03245e77f",
    "dyly" : "",
};
var opaySecrets = {
    "sghj" : "c3e459315a0a4a78",
    "jdwx" : "ff8396b03245e77f",
    "xyl" : "",
    "dyly" : "8a8a80ffb1f051dd",
};

function setConfig() {
    var dangerousVer = document.getElementsByName("DANGEROUS_PAY_VERSION")[0];
    var payType = document.getElementsByName("paytype")[0];
    var serverSecret = document.getElementsByName("server_secret")[0];
    var urlObj = document.getElementsByName("url")[0];
    var redPoint = document.getElementsByName("red_point")[0];

    var appKey = document.getElementsByName("appkey")[0];
    var owpayAES = document.getElementsByName("owpay_aeskey")[0];
    var owpayType = document.getElementsByName("owpay_type")[0];
    var payinfoSecret = document.getElementsByName("payinfo_secret")[0];

    var opayType = document.getElementsByName("opay_type")[0];
    var opaySecret = document.getElementsByName("opay_server_secret")[0];

    redPoint.value = "1";
    dangerousVer.value = "0";
    payType.value = "1";
    statusObj.value = "1";
    enable_register.value = "1";
    enable_pay.value = "1";
    proxyUrl.value = "unknown";
    var sdk = sdkId.value;
    urlObj.value = prefixUrl + urls[sdk] + "/" + gameShorName + "/" + chnId.value;
    sdkName.value = sdkNames[sdk];
    packageName.value = packageNames[sdk];
    serverSecret.value = serverSecrets[gameShorName];
    switch (sdk) {
        case "10019":
            opayType.value = "{\"zfb\":{\"enable\":1,\"discount\":100},\"zwxpay\":{\"enable\":1,\"discount\":100},\"zfb_wap\":{\"enable\":1,\"discount\":100},\"iap\":{\"enable\":0,\"discount\":100}}";
            opaySecret.value = opaySecrets[gameShorName];
        break;
        case "10024":
        case "10025":
            appKey.value = appKeys[gameShorName];
            owpayAES.value = "09f5e8f7fc1a0d27a14521b6c96266hg";
            owpayType.value = "{\"iap\":{\"enable\":0},\"zfb\":{\"enable\":1},\"zwx\":{\"enable\":1}}";
            payinfoSecret.value = "13cedd4db5f92f41";
        break;
    }
}

chnId.addEventListener("change", function(){
    var urlObj = document.getElementsByName("url")[0];
    urlObj.value = prefixUrl + urls[sdk] + "/" + chnId.value;;
});
sdkId.addEventListener("change", function() {
    setTimeout(setConfig, 100);
});
chnId.value = "1001900001";
sdkId.value = "10019";
var ev = document.createEvent("HTMLEvents");  
ev.initEvent("change", false, true);  
sdkId.dispatchEvent(ev);  