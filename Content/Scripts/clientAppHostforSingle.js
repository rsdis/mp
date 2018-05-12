
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

//MessageHub-发送消息
//reboot-重启
//shutdown-关机
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


$("body").contextmenu(function () {
    return false;
});