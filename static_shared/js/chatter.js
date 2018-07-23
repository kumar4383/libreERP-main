document.addEventListener("DOMContentLoaded", function(event) {

  var connection = new autobahn.Connection({url: 'ws://162.168.1.105:8000/ws', realm: 'default'});

  connection.onopen = function (session) {

     console.log("session established!");

     function supportChatResponse() {
       console.log('in supportChatResponse');
     }

    session.subscribe('support.chat', supportChatResponse).then(
      function (sub) {
        console.log("subscribed to topic 'support.chat'");
      },
      function (err) {
        console.log("failed to subscribed: " + err);
      }
    );

  };

  connection.open();


   function getBrowserName() {
     var name;
     if((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1 ){
       name = 'Opera'
     }else if (navigator.userAgent.indexOf("Chrome") != -1 ) {
       name = 'Chrome'
     }else if (navigator.userAgent.indexOf("Safari") != -1) {
       name = 'Safari'
     }else if (navigator.userAgent.indexOf("Firefox") != -1) {
       name = 'Firefox'
     }else if ((navigator.userAgent.indexOf("MSIE") != -1 ) || (!!document.documentMode == true )) {
       name = 'IE'
     }else {
       name = 'unknown'
     }
     return name
   }

   var broswer = getBrowserName()
   var uid = document.title+'$'+broswer
   console.log(uid);




  var body = document.getElementsByTagName("BODY")[0];
  var div = document.createElement("div");
  div.innerHTML = '<div class="chatWindow" style="height:36px;right:30px;" id="chatWindowelizabeth">'+
  '<div class="header" >'+
    '<div class="container-fluid" style="padding:7px;" >'+
      '<i class="fa fa-circle onlineStatus" style="color: #0b8640;font-size: 15px;" ></i>'+
      '<span class="username" style="padding-left:7px; font-size:15px;" >Online</span>'+
      '<span class="pull-right" style="cursor:pointer; font-size:15px;"><i class="fa fa-chevron-down" id="toggle" ></i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i class="fa fa-close" id="closeChatWindow" ></i></span>'+
    '</div>'+
  '</div>'+
  '<div id="messages" class="messageView container-fluid">'+
  '</div>'+
  '<div id="footer"  class="footer">'+
    '<div class="container-fluid input-group" id="footerInputGrp" style="padding:10px;" >'+
      '<input id="inputText" class="form-control" style="width:100%" type="text" >'+
      '<input id="filePicker" type="file" style="display:none;" accept="image/*" />'+
      '<span id="paperClip" class="input-group-addon btn btn-default " style="border:none; border-radius: 0px;"><i class="fa fa-paperclip" aria-hidden="true"></i></span>'+
      '<span id="fileName" class="input-group-addon btn btn-default" style="font-size:10px;" > filename </span>'+
      '<span id="removeFile" class="input-group-addon btn btn-default" style="cursor:pointer" > <i class="fa fa-times" aria-hidden="true"></i> </span>'+
      '<span id="sendFile" class="input-group-addon btn btn-default " style="cursor:pointer"><i class="fa fa-paper-plane-o" aria-hidden="true"></i></span>'+
    '</div>'+
  '</div>'+
  '</div>'

  body.appendChild(div);



  (function () {
    var toggle = true;
    document.getElementById("chatWindowelizabeth").style.height = "36px";
    document.getElementById("footer").style.display = "none";
    document.getElementById("fileName").style.display = "none";
    document.getElementById("removeFile").style.display = "none";
    document.getElementById("sendFile").style.display = "none";
  }());

  document.getElementById("toggle").addEventListener("click", toggleWindow, false);
  document.getElementById("paperClip").addEventListener("click", filePicker, false);

  function filePicker() {
    document.getElementById('filePicker').click();
  }

  function toggleWindow() {
    toggle = !toggle;
    if (toggle) {
      document.getElementById("chatWindowelizabeth").style.height = "500px";
      document.getElementById("footer").style.display = "block";
    }else {
      document.getElementById("chatWindowelizabeth").style.height = "36px";
      document.getElementById("footer").style.display = "none";
    }
  }


  var chat = {user : 'visitor1', messages : [{msg : "Hello..", sentByMe:false , created: new Date("July 18, 2018 01:15:00")} , {msg : "", sentByMe:false , created: new Date("July 18, 2018 01:15:00") , img:'/static/images/appStore.png' } , { msg : "How can i help you?", sentByMe:false, created: new Date()} ] }

  function messageDiv(message) {
    var col = message.sentByMe ? 'col-md-offset-2 col-md-10':'col-md-10'
    var floatSide = message.sentByMe ?  'right':'left'
    var borderRad = message.sentByMe ? '20px 0px 20px 20px':'0px 20px 20px 20px'
    var bgCol = message.sentByMe ? '#dba4ae':'#72b3d4'
    var timeAgoSpan = message.sentByMe ? '<span class="text-muted pull-right" style="font-size:10px; padding-right:25px;">2 days ago</span>':'<span class="text-muted pull-left" style="font-size:10px; padding-left:25px;">5 mins ago</span>'

    var msgDiv = message.msg=='' ? '<img  src="'+ message.img +'" style="width:200px;">' : '<p style="word-break: break-all !important;">'+ message.msg +'</p>'

    msgHtml = '<div class="row">'+
      '<div class="'+ col +'"> '+
        '<div style="float:'+ floatSide +'; background-color:'+ bgCol +'; padding:10px;margin:8px; border-radius:'+ borderRad +'" >'+
          msgDiv +
        '</div>'+
      '</div>'+
    '</div>'+
    '<div class="row">'+
      timeAgoSpan +
    '</div>'
    return msgHtml;
  }


  function pushMessges() {
    for (var i = 0; i < chat.messages.length; i++) {
      var div = document.createElement("div");
      div.innerHTML = messageDiv(chat.messages[i])
      var msg = document.getElementById("messages");
      msg.appendChild(div);
    }
    scroll();
  }
  pushMessges();

  function scroll() {
    setTimeout(function () {
      var id = document.getElementById("messages");
      id.scrollTop = id.scrollHeight;
    }, 200);
  }


  document.getElementById("removeFile").addEventListener("click", removeFile, false);
  document.getElementById("sendFile").addEventListener("click", sendFile, false);


  function removeFile() {
    document.getElementById('filePicker').value = "";

    document.getElementById("fileName").style.display = "none";
    document.getElementById("removeFile").style.display = "none";
    document.getElementById("sendFile").style.display = "none";

    document.getElementById("inputText").style.display = "";
    document.getElementById("paperClip").style.display = "";
  }

  function sendFile() {
    var message = {msg:'' ,  sentByMe:true , created: new Date() , img: '/static/images/career.jpg' }
    var div = document.createElement("div");
    div.innerHTML = messageDiv(message)
    var msg = document.getElementById("messages");
    msg.appendChild(div);
    scroll();

    document.getElementById('filePicker').value = "";
    document.getElementById("fileName").style.display = "none";
    document.getElementById("removeFile").style.display = "none";
    document.getElementById("sendFile").style.display = "none";

    document.getElementById("inputText").style.display = "";
    document.getElementById("paperClip").style.display = "";
  }


  document.getElementById('filePicker').onchange = function(e) {

    var file = document.getElementById('filePicker');

    document.getElementById("inputText").style.display = "none";
    document.getElementById("paperClip").style.display = "none";

    document.getElementById("fileName").style.display = "";
    document.getElementById("removeFile").style.display = "";
    document.getElementById("sendFile").style.display = "";
    document.getElementById("fileName").innerHTML = file.files[0].name;

  }

  var inputText = document.getElementById("inputText");
  inputText.addEventListener("keydown", function (e) {
      if (e.keyCode === 13) {
        if (inputText.value.length>0) {
          var message = {msg:inputText.value ,  sentByMe:true , created: new Date() }
          var div = document.createElement("div");
          div.innerHTML = messageDiv(message)
          var msg = document.getElementById("messages");
          msg.appendChild(div);
          scroll();
          // connection.session.publish($scope.roomID, [$scope.lastItem], {}, {
          //   acknowledge: true
          // }).
          // then(function(publication) {
          //   console.log("Published");
          // });
        }
        inputText.value =''
      }
  }, false);


  document.getElementById("closeChatWindow").addEventListener("click", function(e) {
    alert('Are you sure?');
    // body.removeChild(div);
  }, false);




});