
console.log("加载JS")

$.connection.hub.url = "http://localhost:9999/signalr";
var ws = $.connection.clientMessageHub;

ws.client.send = function (message) {
    console.log(message);
    OnMessage(message);
};

$.connection.hub.start().done(function () {
    console.log("socket 加载完毕");
});

function getAllContentInfos(callback) {
    $.get("http://127.0.0.1:8080/contentinfos", function (data, status) {
        console.log(data);
        callback(data);
    });
}

function getQrByUnique(unique) {
    var url = "http://127.0.0.1:8080/qrByUnique/" + unique;
    var result;
    $.ajax({
        url: url,
        cache: false,
        async: false,
        type: "get",
        dataType: 'json',
        success: function (result) {
            result = result;
        }
    });
    return result;
}

function getAllQrs(callback) {
    var url = "http://127.0.0.1:8080/qrInfos";
    $.ajax({
        url: url,
        cache: false,
        async: false,
        type: "get",
        dataType: 'json',
        success: function (result) {
            console.log(result);
            callback(result);
        }
    });
}


function getAllProductInfos(callback) {
    $.get("http://127.0.0.1:8080/productInfos", function (data, status) {
        console.log(data);
        callback(data);
    });
}

//MessageHub-发送消息
//reboot-重启
//shutdown-关机
//type: switchApp  切换应用
//{type: "", data: ""}
function SendMessage(json) {
    if (ws != undefined) {
        ws.server.receiveCommand(json);
    }
}

//MessageHub获取消息（必须要实现的JS方法）
/*
 * MessageType
 *     0:ReloadChrome   
 */
function OnMessage(json) {
    var obj = JSON.parse(json);
    if (obj.MessageType === 0) {
        window.location.href = obj.MessageData;
        console.log(obj.MessageData);
    }

}

//初始化页面中的菜单
function initRingMenu(data) {
    getAllProductInfos(function (product) {
        $.get("/Content/Scripts/menuItemTmpl.html", function (tmpl) {
            var menuList = data;
            if (menuList.length > 0) {
                menuList = { menuList: menuList, hostBasicPath: product.HostBasicPath };
                var ringTmpl = $.templates(tmpl);
                var html = ringTmpl.render(menuList);

                $("body").append(html);

                var items = $(".menuItem");
                for (var i = 0, l = items.length; i < l; i++) {
                    items[i].style.left = (50 - 35 * Math.cos(-0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";

                    items[i].style.top = (50 + 35 * Math.sin(-0.5 * Math.PI - 2 * (1 / l) * i * Math.PI)).toFixed(4) + "%";
                }

                $(".circle .center").unbind("click");
                $(".circle .center").bind("click", function (e) {
                    openCircle(e);
                })
            }
        })
    })
}

function gotoApp(url, id) {
    var json = {
        type: "switchApp",
        data: id
    }
    SendMessage(json);
    location.href = url;
}

function openCircle(e) {
    if ($(".circle").hasClass("open")) {
        if (!e) {
            util.closeCircleAction();
        }
    } else {
        tmpTop = $(".circle").css("top");
        tmpLeft = $(".circle").css("left");
        $(".circle").removeAttr("style");
        $(".circle").addClass("open");
        // draggableDisable();

        if (e) {
            $(document).unbind("click");
            $(document).bind("click", function () {
                closeCircleAction();
                $(document).unbind("click");
                // clearInterval(backKeylookInterval);
            });

            e.stopPropagation();
        }
    }
}

function closeCircleAction() {
    $(".circle").css({
        "top": tmpTop,
        "left": tmpLeft
    });
    $(".circle").removeClass("open");
    // draggableEnable();
}

function openCirclrAction() {
    tmpTop = $(".circle").css("top");
    tmpLeft = $(".circle").css("left");
    $(".circle").removeAttr("style");
    $(".circle").addClass("open");
    // draggableDisable();
}

$(function () {
    getAllContentInfos(initRingMenu);
})


$("body").contextmenu(function () {
    return false;
});