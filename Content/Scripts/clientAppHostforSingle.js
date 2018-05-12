
console.log("加载JS")

var ws = new WebSocket("ws://127.0.0.1:9999/");
ws.onmessage = function (event) {
    console.log(event.data)
    OnMessage(event.data)
};

//MessageHub-发送消息
//reboot-重启
//shutdown-关机
function SendMessage(json) {
    $.post("http://127.0.0.1:8080/api/post_msg", json,function (result) {
        console.log(data)
    });
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