window.InjectCode = function() {
    function $(name) {
        return document.getElementsByName(name)[0];
    }
    return {
        sdkName : $("sdk_name"),
        gameType : $("game_type"),
        packageName : $("package_name"),
        proxyUrl : $("proxy_url"),
        chnId : $("chn_id"),
        sdkId : $("sdk_id"),
        statusObj : $("status"),
        enable_register : $("enable_register"),
        enable_pay : $("enable_pay"),
        gameShorName : window.location.host.split(".")[0],
        prefixUrl : "http://fxcb.umipay.com/",
        resultDiv : "",
        _this : "",
        urls : {
            "10019" : "opay_iap",
            "10024" : "owpay_iap",
            "10025" : "h5",
        },
        sdkNames : {
            "10019" : "iapopay",
            "10024" : "owpay_iap",
            "10025" : "h5",
        },
        packageNames : {
            "10019" : "xxx.iapopay",
            "10024" : "xxx.ow",
            "10025" : "xxx.h5",
        },
        /// appid 运营那边给
        appKeys : {
            "sghj" : "b780142b09f59a04",
            "jdwx" : "8b1c0b73738d40b7",
            "xyl" : "5b4c87a34471065f",
            "dyly" : "4c71a5fd2986ef89",
        },
        /// server_secret 运营那边给
        serverSecrets : {
            "sghj" : "71207e5bda1f8d1d",
            "jdwx" : "69da2a872ce86982",
            "xyl" : "ff8396b03245e77f",
            "dyly" : "",
        },
        /// 在 https://owadm.ouwan.cn/pay/opay/game/list/ 这里面找，没有就新建一个
        opaySecrets : {
            "sghj" : "c3e459315a0a4a78",
            "jdwx" : "3c42a831f8dc65c1",
            "xyl" : "b4bbd3ec1f03c473",
            "dyly" : "8a8a80ffb1f051dd",
        },
        init : function() {
            _this = this;
            _this.chnId.addEventListener("change", function() {
                _this.setUrl(_this.sdkId.value);
                _this.showResult();
            });
            _this.gameType.addEventListener("change", function() {
                _this.showResult();
            });
            _this.sdkId.addEventListener("change", function() {
                setTimeout(_this.setConfig, 200);
                _this.showResult();
            });
            _this.chnId.value = "1001900001";
            _this.sdkId.value = "10019";
            /// 显示参数结果，是要给到运营那边的参数，显示出来方便整理。
            _this.resultDiv = document.createElement("div");
            _this.resultDiv.setAttribute("id", "resultDiv");
            _this.resultDiv.setAttribute("style", "color: white; background-color: black; padding: 20px;");
            document.getElementById("sidebar").appendChild(_this.resultDiv);

            var ev = document.createEvent("HTMLEvents");
            ev.initEvent("change", false, true);
            _this.sdkId.dispatchEvent(ev);
        },
        setUrl : function(sdk) {
            /// http://fxcb.umipay.com/sdk名/游戏名/渠道号
            $("url").value = _this.prefixUrl + _this.urls[sdk] + "/" + _this.gameShorName + "/" + _this.chnId.value;
        },
        setConfig : function() {
            $("DANGEROUS_PAY_VERSION").value = "0";
            $("paytype").value = "1";
            $("red_point").value = "1";
            _this.proxyUrl.value = "unknown";
            _this.statusObj.value = "1";
            _this.enable_register.value = "1";
            _this.enable_pay.value = "1";
            
            var sdk = _this.sdkId.value;
            _this.sdkName.value = _this.sdkNames[sdk];
            _this.packageName.value = _this.packageNames[sdk];
            $("server_secret").value = _this.serverSecrets[_this.gameShorName];
            /// 渠道号格式：1001900001, 1001900002, ..., 1001900010
            if (!_this.chnId.value.startsWith(sdk)) {
                _this.chnId.value = sdk + "00001";
            }
            _this.setUrl(sdk);

            switch (sdk) {
                case "10019":
                    $("opay_type").value = "{\"zfb\":{\"enable\":1,\"discount\":100},\"zwxpay\":{\"enable\":1,\"discount\":100},\"zfb_wap\":{\"enable\":1,\"discount\":100},\"iap\":{\"enable\":0,\"discount\":100}}";
                    $("opay_server_secret").value = _this.opaySecrets[_this.gameShorName];
                break;
                case "10024":
                case "10025":
                    $("appkey").value = _this.appKeys[_this.gameShorName];
                    /// 后台给参数
                    $("owpay_aeskey").value = "09f5e8f7fc1a0d27a14521b6c96266hg";
                    $("owpay_type").value = "{\"iap\":{\"enable\":0},\"zfb\":{\"enable\":1},\"zwx\":{\"enable\":1}}";
                    $("payinfo_secret").value = "13cedd4db5f92f41";
                break;
            }
        },
        showResult: function() {
            _this.resultDiv.innerHTML = _this.gameType.options[_this.gameType.selectedIndex].title + "<br>" + "渠道号 " + _this.chnId.value + "<br>" + "子渠道号 0";
            var input = document.createElement("input");
            document.body.appendChild(input);
            input.setAttribute("value", _this.resultDiv.innerHTML.replace(/<br>/g, "\r\n"));
            input.select();
            document.execCommand("copy");
            console.log("复制成功");
        },
    };
}();
window.InjectCode.init();
