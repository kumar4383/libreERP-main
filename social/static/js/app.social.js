app.directive('commentBubble', function () {
  return {
    templateUrl:'/static/ngTemplates/commentBubble.html',
    restrict: 'E',
    transclude: true,
    replace:true,
    scope:{
      data : '=',
      onDelete : '&',
    },
    controller : function($scope, $http , userProfileService){
      $scope.me = userProfileService.get("mySelf");
      $scope.liked = false;
      for (var i = 0; i < $scope.data.likes.length; i++) {
        if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
          $scope.liked = true;
          break;
        }
      }
      if ($scope.data.user.cleanUrl()==$scope.me.url){
        $scope.iCommented = true;
      } else {
        $scope.iCommented = false;
      }
      $scope.like = function(){
        if ($scope.liked) {
          for (var i = 0; i < $scope.data.likes.length; i++) {
            if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
              index = i;
              // console.log($scope.data.likes[i]);
              $http({method: 'DELETE', url: $scope.data.likes[i].url}).
                then(function(response , index) {
                  $scope.data.likes.splice(index, 1);
                  $scope.liked = false;
                }, function(response) {
                  // console.log("failed to sent the comment");
              });
            }
          }
        } else {
          dataToSend = {parent: $scope.data.url.cleanUrl() , user: $scope.data.user};
          // although the api will set the user to the sender of the request a valid user url is needed for the request otherwise 400 error will be trown
          $http({method : 'PATCH' , url : $scope.data.url }).
          then(function(response){
            // console.log(response);
            for (var i = 0; i < response.data.likes.length; i++) {
              if (response.data.likes[i].user.cleanUrl() == $scope.me.url){
                $scope.data.likes.push(response.data.likes[i])
              }
            }
            $scope.liked = true;
          }, function(response){

          });
        }
      }
      $scope.delete = function(){
        $http({method : 'DELETE' , url : $scope.data.url }).
        then(function(response){
          $scope.onDelete();

        }, function(response){

        });
      }
    },
  };
});

app.directive('post', function () {
  return {
    templateUrl: '/static/ngTemplates/postBubble.html',
    restrict: 'E',
    transclude: true,
    replace:true,
    scope:{
      data : '=',
      onDelete :'&',
    },
    controller : function($scope, $http , $timeout , userProfileService , $aside , $interval , $window) {
      $scope.openPost = function(position, backdrop , input) {
        $scope.asideState = {
          open: true,
          position: position
        };

        function postClose() {
          $scope.asideState.open = false;
        }

        $aside.open({
          templateUrl: '/static/ngTemplates/app.social.aside.post.html',
          placement: position,
          size: 'md',
          backdrop: backdrop,
          controller:'controller.social.aside.post',
          resolve: {
           input: function () {
             return input;
            }
          }
        }).result.then(postClose, postClose);
      }
    },
  };
});

app.controller('controller.social.aside.post' , function($scope, $uibModalInstance , $http, userProfileService , input) {
  $scope.content = 'post';
  var emptyFile = new File([""], "");
  $scope.me = userProfileService.get("mySelf");
  $scope.data = input.data;
  $scope.onDelete = input.onDelete;

  if (typeof $scope.data.url == 'undefined') {
    return;
  }
  postUrl = $scope.data.url
  if ($scope.onDelete.length != 0){ // if the post aside is initiated by the notification system then the refreshed data is already fetched by it
    // and passed into input as data
    postUrl += '&user='+userProfileService.get($scope.data.user).username;
    $http({method: 'GET' , url : postUrl}).
    then(function(requests){
      for(key in requests.data){
        $scope.data[key] = requests.data[key];
      }
    });
  }
  setTimeout(function () {
    scroll("#commentsArea");
  }, 100);
  $scope.possibleCommentHeight = 70; // initial height percent setting
  $scope.textToComment = "";
  var tagged = '';
  for (var i = 0; i < $scope.data.tagged.length; i++) {
    tagged  += userProfileService.get($scope.data.tagged[i]).username;
    if (i != $scope.data.tagged.length-1){
      tagged += ',';
    }
  }
  $scope.postEditor = {attachment : emptyFile , tagged : tagged}
  $scope.viewMode = 'comments';
  $scope.liked = false;
  if (typeof $scope.data == 'undefined') {
    return;
  }
  for (var i = 0; i < $scope.data.likes.length; i++) {
    if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
      $scope.liked = true;
      break;
    }
  }
  if ($scope.data.user.cleanUrl() == $scope.me.url) {
    $scope.isOwner = true;
  } else {
    $scope.isOwner = false;
  }
  setTimeout(function () {
    postBodyHeight = $("#postModalBody").height();
    inputHeight = $("#commentInput").height();
    winHeight = $(window).height();
    defaultHeight = postBodyHeight + 5.7*inputHeight;
    $scope.commentsHeight = Math.floor(100*(winHeight - defaultHeight)/winHeight);
    $scope.$apply();
    scroll("#commentsArea");
  }, 100);

  $scope.refreshAside = function(signal){

    var nodeUrl = '/api/social/';
    if (signal.action == 'created') {
      if (typeof signal.parent == 'number'){
        updateType = signal.type.split('.')[1];

        if (updateType == 'commentLike') {
          pk = signal.parent;
          url = nodeUrl + $scope.content + 'Comment';
        } else {
          pk = signal.id;
          url = nodeUrl + updateType;
        }
        $http({method : 'GET' , url : url + '/' + pk +'/'}).
        then(function(response){
          if (response.data.parent == $scope.data.url.cleanUrl()) {
            if (updateType == $scope.content + 'Like') {
              $scope.data.likes.push(response.data);
              if (response.data.user == $scope.me.url) {
                $scope.liked = true;
              }
            } else if (updateType == $scope.content+ 'Comment') {
              $scope.data.comments.push(response.data);
            } else if (updateType == 'commentLike') {
              $http({method : 'GET' , url : nodeUrl + updateType + '/' + signal.id +'/'}).
              then(function(response){
                for (var i = 0; i < $scope.data.comments.length; i++) {
                  if( $scope.data.comments[i].url.indexOf(url + '/' + pk +'/') != -1) {
                    $scope.data.comments[i].likes.push(response.data);
                  }
                }
              })
            }
          }
        });
      } else {
        $http({method : 'GET' , url : '/api/PIM/notification/' + signal.id +'/'}).
        then(function(response){
          parts = response.data.shortInfo.split(':');
          updateType = parts[0];
          if (updateType == $scope.content + 'Like') {
            $http({method : 'GET' , url : '/api/social/'+ $scope.content +'Like/' + parts[1] +'/'}).
            then(function(response){
              if (response.data.parent == $scope.data.url.cleanUrl()) {
                $scope.data.likes.push(response.data);
                if (response.data.user == $scope.me.url) {
                  $scope.liked = true;
                }
              }
            });
          }else if (updateType == $scope.content + 'Comment') {
            $http({method : 'GET' , url : '/api/social/' + $scope.content + 'Comment/' + parts[1] +'/'}).
            then(function(response){
              if (response.data.parent == $scope.data.url.cleanUrl()) {
                $scope.data.comments.push(response.data);
              }
            });
          };
        });
      }
    }else if (signal.action == 'deleted'){
      if (typeof signal.parent == 'number'){
        id = signal.id;

      }else{
        id = signal.objID;
      }
      updateType = signal.type.split('.')[1];
      if (updateType == $scope.content + 'Comment') {

        for (var i = 0; i < $scope.data.comments.length; i++) {
          if ($scope.data.comments[i].url.indexOf( nodeUrl + updateType + '/'+ id) != -1){
            $scope.data.comments.splice(i, 1);
          }
        }
      } else if (updateType == $scope.content + 'Like') {

        for (var i = 0; i < $scope.data.likes.length; i++) {
          if ($scope.data.likes[i].url.indexOf( nodeUrl + updateType + '/'+ id) != -1){
            $scope.data.likes.splice(i, 1);
            for (var i = 0; i < $scope.data.likes.length; i++) {
              if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
                $scope.liked = true;
                break;
              }
            }
          }
        };
      } else if (updateType == 'commentLike') {
        for (var i = 0; i < $scope.data.comments.length; i++) {
          for (var j = 0; j < $scope.data.comments[i].likes.length; j++) {
            // console.log(nodeUrl + updateType + '/' + signal.id);
            if($scope.data.comments[i].likes[j].url.indexOf(nodeUrl + updateType + '/' + signal.id) != -1) {
              $scope.data.comments[i].likes.splice(j,1);
            }
          }
        }
      }
    } // if - else
    setTimeout(function () {
      scroll("#commentsArea");
    }, 1000);
  };
  $scope.comment = function(){
    if ($scope.textToComment == "") {
      return;
    }
    dataToSend = {text: $scope.textToComment , parent: $scope.data.url.cleanUrl() , user: $scope.data.user };
    // although the api will set the user to the sender of the request a valid user url is needed for the request otherwise 400 error will be trown
    $http({method: 'POST', data:dataToSend, url: '/api/social/postComment/'}).
      then(function(response) {
        $scope.data.comments.push(response.data)
        $scope.textToComment = "";
        $scope.viewMode = 'comments';
        setTimeout(function () {
          scroll("#commentsArea");
        }, 100);
      }, function(response) {
        // console.log("failed to sent the comment");
    });
  }
  $scope.deleteComment = function(index){
    $scope.data.comments.splice(index , 1);
  }

  $scope.like = function(){
    if ($scope.liked) {
      $http({method: 'DELETE', url: $scope.data.likes[i].url}).
        then(function(response) {
          for (var i = 0; i < $scope.data.likes.length; i++) {
            if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
              $scope.data.likes.splice(i, 1);
              $scope.liked = false;
            }
          }
        }, function(response) {
          // console.log("failed to sent the comment");
      });

    } else {
      dataToSend = {parent: $scope.data.url.cleanUrl() , user: $scope.data.user};
      // although the api will set the user to the sender of the request a valid user url is needed for the request otherwise 400 error will be trown
      $http({method: 'POST', data:dataToSend, url: '/api/social/postLike/'}).
        then(function(response) {
          $scope.liked = true;
          $scope.data.likes.push(response.data)
        }, function(response) {
          // console.log("failed to sent the comment");
      });
    }
  }
  $scope.enableEdit = function(){
    $scope.editMode = true;
    $scope.backupText = angular.copy($scope.data.text);
  }
  $scope.save = function(){
    var fd = new FormData();
    fd.append('text' , $scope.data.text );
    fd.append('user' , $scope.me.url);
    if ($scope.postEditor.attachment !=emptyFile) {
      fd.append('attachment' , $scope.postEditor.attachment);
    }
    if ( typeof $scope.postEditor.tagged !='undefined' && $scope.postEditor.tagged != '' ) {
      fd.append('tagged' , $scope.postEditor.tagged)
    }

    var url = $scope.data.url;
    $http({method : 'PATCH' , url : url, data : fd , transformRequest: angular.identity, headers: {'Content-Type': undefined}}).
    then(function(response){
      $scope.editMode = false;
      for(key in response.data){
        $scope.data[key] = response.data[key];
      }
    });
  }
  $scope.cancelEditor = function(){
    $scope.data.text = $scope.backupText;
    $scope.editMode = false;
  }

  $scope.delete = function(){
    $http({method : 'DELETE' , url : $scope.data.url}).
    then(function(response){
      $scope.onDelete();
      $uibModalInstance.close();
    });
  }
});

app.directive('album', function () {
  return {
    template:'<li>'+
        '<i class="fa fa-camera bg-aqua"></i>'+
        '<div class="timeline-item">'+
          '<span class="time"><i class="fa fa-clock-o"></i> {{data.created | timeAgo}} ago</span>'+
          '<h3 class="timeline-header"><a href="#">{{data.user | getName}}</a> uploaded new photos to album : {{data.title}}</h3>'+
          '<div class="timeline-body">'+
            '<div ng-repeat = "picture in data.photos" style="display: inline;">'+
              '<img ng-click="openAlbum('+"'right'"+ ', true , {data : picture , parent : data , onDelete : albumDelete})" ng-src="{{picture.photo}}" alt="..." class="margin" height="100px" width="150px" >'+
            '</div>'+
          '</div>'+
        '</div>'+
      '</li>',
    restrict: 'E',
    transclude: true,
    replace:true,
    scope:{
      data : '=',
      albumDelete :'&',
    },
    controller : function($scope, $http , $timeout , userProfileService , $aside , $interval , $window) {
      $scope.openAlbum = function(position, backdrop , input) {
        $scope.asideState = {
          open: true,
          position: position
        };

        function postClose() {
          $scope.asideState.open = false;
        }

        $aside.open({
          templateUrl: '/static/ngTemplates/app.social.aside.album.html',
          placement: position,
          size: 'lg',
          backdrop: backdrop,
          controller: 'controller.social.aside.picture',
          resolve: {
           input: function () {
             return input;
            }
          }
        }).result.then(postClose, postClose);
      }
    },
  };
});

app.controller('controller.social.aside.picture' , function($scope, $uibModalInstance , Flash , $http , userProfileService , input) {

  $scope.content = 'picture';
  $scope.me = userProfileService.get("mySelf");
  $scope.data = input.data;
  $scope.parent = input.parent;
  $scope.albumDelete = input.onDelete;
  if ($scope.data.url.indexOf('?')==-1) {
    $scope.data.url += '?';
  }
  $http({method: 'GET' , url : $scope.data.url + '&user=' + userProfileService.get($scope.data.user).username}).
  then(function(requests){
    for(key in requests.data){
      $scope.data[key] = requests.data[key];
    }
    setTimeout(function () {
      scroll("#commentsArea");
    }, 100);
  });
  $http({method: 'GET' , url : $scope.parent.url + '&user=' + userProfileService.get($scope.data.user).username}).
  then(function(requests){
    for(key in requests.data){
      $scope.parent[key] = requests.data[key];
    }
  });
  $scope.views = [{name : 'drag' , icon : '' , template : '/static/ngTemplates/draggablePhoto.html'} ];
  $scope.getParams = [{key : 'albumEditor', value : ''}, {key : 'user' , value : $scope.me.username}];
  $scope.droppedObjects = angular.copy($scope.parent.photos);
  var tagged = '';
  for (var i = 0; i < $scope.parent.tagged.length; i++) {
    tagged  += userProfileService.get($scope.parent.tagged[i]).username;
    if (i != $scope.parent.tagged.length-1){
      tagged += ',';
    }
  }
  $scope.tempAlbum = {title :  $scope.parent.title , photos : [] , tagged : tagged};
  $scope.editorData = {draggableObjects : []};
  $scope.editMode = false;
  $scope.possibleCommentHeight = 70;
  $scope.toComment = {textToComment : ''};
  $scope.viewMode = 'comments';
  $scope.liked = false;
  for (var i = 0; i < $scope.data.likes.length; i++) {
    if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
      $scope.liked = true;
      break;
    }
  }
  if ($scope.data.user.cleanUrl() == $scope.me.url && $scope.parent != 'empty') {
    $scope.isOwner = true;
  } else {
    $scope.isOwner = false;
  }
  setTimeout(function () {
    postBodyHeight = $("#postModalBody").height();
    inputHeight = $("#commentInput").height();
    winHeight = $(window).height();
    defaultHeight = postBodyHeight + 6*inputHeight;
    $scope.commentsHeight = Math.floor(100*(winHeight - defaultHeight)/winHeight);
    $scope.$apply();
    scroll("#commentsArea");
  }, 100);
  $scope.comment = function(){
    if ($scope.toComment.textToComment == 's') {
      return;
    }
    dataToSend = {text: $scope.toComment.textToComment , parent: $scope.data.url.cleanUrl() , user: $scope.data.user };
    // although the api will set the user to the sender of the request a valid user url is needed for the request otherwise 400 error will be trown
    $http({method: 'POST', data:dataToSend, url: '/api/social/pictureComment/'}).
      then(function(response) {
        $scope.toComment.textToComment = "";
        $scope.data.comments.push(response.data)
        $scope.viewMode = 'comments';
        setTimeout(function () {
          scroll("#commentsArea");
        }, 100);
      }, function(response) {
        // console.log("failed to sent the comment");

    });
  }
  $scope.deletePhoto = function(){
    $http({method : 'DELETE' , url : $scope.data.url}).
    then(function(response){
      for (var i = 0; i < $scope.parent.photos.length; i++) {
        if ($scope.parent.photos[i].url == $scope.data.url){
          $scope.parent.photos.splice(i, 1);
          if (i == 0 && $scope.parent.photos.length == 0) {
            $scope.deleteAlbum()
          }else{
            if ($scope.parent.photos.length <= i+1) {
              $scope.data = $scope.parent.photos[i-1];
            } else {
              $scope.data = $scope.parent.photos[i];
            }
          }
        }
      }
    } , function(response){

    });
  }
  $scope.edit = function(){
    $scope.editMode = true;
  }
  $scope.cancelEditor = function(){
    $scope.editMode = false;
  }
  $scope.deleteAlbum = function(){
    $http({method : 'DELETE' , url : $scope.parent.url}).
    then(function(response){
      $scope.albumDelete();
      // calling the album Delete function passed with the open Album Aside function to refresh the feeds
      $uibModalInstance.close();
    } , function(response){

    });
  }
  $scope.deleteComment = function(index){
    $scope.data.comments.splice(index , 1);
  }
  $scope.removeFromTempAlbum = function(index){
    pic = $scope.droppedObjects[index];
    $scope.droppedObjects.splice(index , 1);
    $scope.editorData.draggableObjects.push(pic);
  }
  $scope.updateAlbum = function(){
    if ($scope.droppedObjects.length == 0) {
      Flash.create('danger', 'No photos in the album' );
      return;
    }
    for (var i = 0; i < $scope.droppedObjects.length; i++) {
      uri = $scope.droppedObjects[i].url.split('/?')[0];
      // nested request is not supported by the django rest framework so sending the PKs of the photos to the create function in the serializer
      pk = uri.split('picture/')[1].split('/')[0];
      $scope.tempAlbum.photos.push(pk);
    }
    dataToPost = {
      user : $scope.me.url,
      title : $scope.tempAlbum.title,
      photos : $scope.tempAlbum.photos,
      tagged : $scope.tempAlbum.tagged,
    };
    // console.log(dataToPost);
    $http({method: 'PATCH' , data : dataToPost , url : $scope.parent.url}).
    then(function(response){
      Flash.create('success', response.status + ' : ' + response.statusText );
      $scope.parent.title = response.data.title;
      $scope.parent.photos = response.data.photos;
      $scope.parent.tagged = response.data.tagged;
    }, function(response){
      Flash.create('danger', response.status + ' : ' + response.statusText );
    });
  }
  $scope.onDropComplete=function(data,evt){
    var index = $scope.droppedObjects.indexOf(data);
    if (index == -1){
      $scope.droppedObjects.push(data);
      var index = $scope.editorData.draggableObjects.indexOf(data);
      $scope.editorData.draggableObjects.splice(index , 1);
    }
  }
  $scope.like = function(){
    if ($scope.liked) {
      for (var i = 0; i < $scope.data.likes.length; i++) {
        if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
          index = i;
          $http({method: 'DELETE', url: $scope.data.likes[i].url}).
            then(function(response , index) {
              $scope.data.likes.splice(index, 1);
              $scope.liked = false;
            }, function(response) {
              // console.log("failed to sent the comment");
          });
        }
      }
    } else {
      dataToSend = {parent: $scope.data.url.cleanUrl() , user: $scope.data.user};
      // although the api will set the user to the sender of the request a valid user url is needed for the request otherwise 400 error will be trown
      $http({method: 'POST', data:dataToSend, url: '/api/social/pictureLike/'}).
        then(function(response) {
          $scope.liked = true;
          $scope.data.likes.push(response.data)
        }, function(response) {
          // console.log("failed to sent the comment");
      });
    }
  }
  $scope.refreshAside = function(signal){
    console.log(signal);

    var nodeUrl = '/api/social/';
    if (signal.action == 'created') {
      if (typeof signal.parent == 'number'){
        updateType = signal.type.split('.')[1];

        if (updateType == 'commentLike') {
          pk = signal.parent;
          url = nodeUrl + $scope.content + 'Comment';
        } else {
          pk = signal.id;
          url = nodeUrl + updateType;
        }
        $http({method : 'GET' , url : url + '/' + pk +'/'}).
        then(function(response){
          if (response.data.parent == $scope.data.url.cleanUrl()) {
            if (updateType == $scope.content + 'Like') {
              $scope.data.likes.push(response.data);
              if (response.data.user == $scope.me.url) {
                $scope.liked = true;
              }
            } else if (updateType == $scope.content+ 'Comment') {
              $scope.data.comments.push(response.data);
            } else if (updateType == 'commentLike') {
              $http({method : 'GET' , url : nodeUrl + updateType + '/' + signal.id +'/'}).
              then(function(response){
                for (var i = 0; i < $scope.data.comments.length; i++) {
                  if( $scope.data.comments[i].url.indexOf(url + '/' + pk +'/') != -1) {
                    $scope.data.comments[i].likes.push(response.data);
                  }
                }
              })
            }
          }
        });
      } else {
        $http({method : 'GET' , url : '/api/PIM/notification/' + signal.id +'/'}).
        then(function(response){
          parts = response.data.shortInfo.split(':');
          updateType = parts[0];
          if (updateType == $scope.content + 'Like') {
            $http({method : 'GET' , url : '/api/social/'+ $scope.content +'Like/' + parts[1] +'/'}).
            then(function(response){
              if (response.data.parent == $scope.data.url.cleanUrl()) {
                $scope.data.likes.push(response.data);
                if (response.data.user == $scope.me.url) {
                  $scope.liked = true;
                }
              }
            });
          }else if (updateType == $scope.content + 'Comment') {
            $http({method : 'GET' , url : '/api/social/' + $scope.content + 'Comment/' + parts[1] +'/'}).
            then(function(response){
              if (response.data.parent == $scope.data.url.cleanUrl()) {
                $scope.data.comments.push(response.data);
              }
            });
          };
        });
      }
    }else if (signal.action == 'deleted'){
      if (typeof signal.parent == 'number'){
        id = signal.id;

      }else{
        id = signal.objID;
      }
      updateType = signal.type.split('.')[1];
      if (updateType == $scope.content + 'Comment') {

        for (var i = 0; i < $scope.data.comments.length; i++) {
          if ($scope.data.comments[i].url.indexOf( nodeUrl + updateType + '/'+ id) != -1){
            $scope.data.comments.splice(i, 1);
          }
        }
      } else if (updateType == $scope.content + 'Like') {

        for (var i = 0; i < $scope.data.likes.length; i++) {
          if ($scope.data.likes[i].url.indexOf( nodeUrl + updateType + '/'+ id) != -1){
            $scope.data.likes.splice(i, 1);
            for (var i = 0; i < $scope.data.likes.length; i++) {
              if ($scope.data.likes[i].user.cleanUrl() == $scope.me.url) {
                $scope.liked = true;
                break;
              }
            }
          }
        };
      } else if (updateType == 'commentLike') {
        for (var i = 0; i < $scope.data.comments.length; i++) {
          for (var j = 0; j < $scope.data.comments[i].likes.length; j++) {
            // console.log(nodeUrl + updateType + '/' + signal.id);
            if($scope.data.comments[i].likes[j].url.indexOf(nodeUrl + updateType + '/' + signal.id) != -1) {
              $scope.data.comments[i].likes.splice(j,1);
            }
          }
        }
      }
    } // if - else
    setTimeout(function () {
      scroll("#commentsArea");
    }, 1000);
  };
});

app.directive('socialProfile', function () {
  return {
    templateUrl: '/static/ngTemplates/app.social.profile.html',
    restrict: 'E',
    replace: false,
    scope: {
      userUrl : '=',
    },
    controller : 'controller.social.profile',
  };
});

app.controller('controller.social.profile', function($scope , $http , $timeout , userProfileService , $aside , $interval , $window , Flash) {
  emptyFile = new File([""], "");
  $scope.me = userProfileService.get('mySelf')
  $scope.user = userProfileService.get($scope.userUrl, true);
  // console.log($scope.me);
  var feedsItems = ['picture'];
  for (var i = 0; i < feedsItems.length; i++){
    mode = feedsItems[i];
    $http({method : 'GET' , url : '/api/social/' + mode +'/?format=json&user='+ $scope.user.username}).
    then(function(response){
      $scope.user.pictures = response.data;
    });
  };

  $scope.offset = {post : 0 , album : 0};
  $scope.max = {post : 0 , album : 0};
  $scope.limit  = 5;
  $scope.socialResource = {posts : [] , albums : []};
  // to get the next or prev five social content in mode = post or album based on the currect value of offset[key] and the limit


  $scope.getFiveStatus = 0;
  $scope.feedStart = 0;

  $scope.$watch('getFiveStatus' , function(newValue , oldValue){
    if (newValue == 2) {
      $scope.sortResource();
      $scope.refreshFeeds();
    }
  });

  $scope.droppedObjects = [];
  $scope.editorData = {draggableObjects : []}; // for the album editor
  $scope.statusMessage = '';
  $scope.picturePost = {photo : {} , tagged : ''};
  $scope.isFollowing = false; // for storing if the user is following the the user whose profile he is visiting
  if ($scope.user.username == $scope.me.username) {
    $scope.myProfile = true;
  }else {
    $scope.myProfile = false;
  }

  $http({method:'GET' , url : $scope.user.social}).then(
    function(response){
      $scope.user.socialData = response.data;
      $scope.user.socialData.coverPicFile = emptyFile;
      for (var i = 0; i < response.data.followers.length; i++) {
        if (response.data.followers[i].cleanUrl() == $scope.me.url.cleanUrl()){
          $scope.isFollowing = true;
        }
      }
    }
  )

  $http({method:'GET' , url : $scope.user.designation}).then(
    function(response){
      $scope.user.designationData = response.data;
    }
  )

  $scope.views = [{name : 'drag' , icon : '' , template : '/static/ngTemplates/draggablePhoto.html'} ]; // to be used in the album editor
  $scope.getParams = [{key : 'albumEditor', value : ''}, {key : 'user' , value : $scope.user.username}];
  $scope.tempAlbum = {title : '' , photos : [] , tagged : ''};

  $scope.openChat = function(){
    $scope.$parent.$parent.$parent.addIMWindow($scope.user.url);
  };

  $scope.follow = function(){
    if ($scope.isFollowing) {
      dataToSend = {friend : $scope.user.username , mode : 'unfollow'}
      $http({method : 'PATCH' , url : $scope.me.social , data : dataToSend }).
      then(function(response){
        $scope.isFollowing = false;
        for (var i = 0; i < $scope.user.socialData.followers.length; i++) {
          if ($scope.user.socialData.followers[i].cleanUrl() == $scope.me.url.cleanUrl()){
            $scope.user.socialData.followers.splice(i,1);
          }
        }
      })
    } else {
      dataToSend = {friend : $scope.user.username , mode : 'follow'}
      $http({method : 'PATCH' , url : $scope.me.social , data : dataToSend }).
      then(function(response){
        $scope.isFollowing = true;
        $scope.user.socialData.followers.push($scope.me.url);
      });
    }
  };

  $scope.getFive = function(mode){
    $http({method : 'GET' , url : '/api/social/' + mode +'/?format=json&user='+ $scope.user.username+'&offset=' + $scope.offset[mode] + '&limit='+$scope.limit}).
    then(function(response){
      $scope.max['post'] = response.data.count;
      if (response.config.url.indexOf('album') != -1) {
        for (var i = 0; i < response.data.results.length; i++) {
          $scope.socialResource.albums.push(response.data.results[i])
        }
        $scope.getFiveStatus +=1;
        $scope.offset['album'] += $scope.limit;
      } else if (response.config.url.indexOf('post') != -1) {
        for (var i = 0; i < response.data.results.length; i++) {
          $scope.socialResource.posts.push(response.data.results[i])
          // console.log(response.data.results[i].text);
        }
        $scope.getFiveStatus +=1;
        $scope.offset['post'] += $scope.limit;
      };
    });
  };

  $scope.getFive('post');
  $scope.getFive('album');

  $scope.sortResource = function(){
    // console.log("now sorting the rawResourceFeeds");
    orderMat = [];
    // console.log( $scope.socialResource.albums);
    for (var i = 0; i < $scope.socialResource.albums.length; i++) {
      orderMat.push( {created : $scope.socialResource.albums[i].created , type: 'album', index : i })
    }
    // console.log($scope.socialResource.posts);
    for (var i = 0; i < $scope.socialResource.posts.length; i++) {
      orderMat.push( {created : $scope.socialResource.posts[i].created , type: 'post', index : i })
    }
    $scope.rawResourceFeeds = angular.copy(orderMat);
    orderMat.sortIndices(function(b, a) { return new Date(a.created).getTime() - new Date(b.created).getTime(); });
    // console.log(orderMat);
    $scope.sortedResourceFeeds = [];
    for (var i = 0; i < orderMat.length; i++) {
      $scope.sortedResourceFeeds.push( $scope.rawResourceFeeds[orderMat[i]] )
    }
    // console.log($scope.sortedResourceFeeds);
  }
  $scope.refreshFeeds = function(){
    // console.log("now refreshing the post");
    $scope.sortedFeeds = [];
    for (var i = 0; i < 5; i++) {
      if ($scope.feedStart + i > $scope.sortedResourceFeeds.length) {
        break;
      }
      $scope.sortedFeeds.push($scope.sortedResourceFeeds[$scope.feedStart+i]);
    }
    // console.log($scope.sortedFeeds);
  }
  $scope.removePost = function(index){
    // console.log("removed post");
    $scope.socialResource.posts.splice(index, 1);
    $scope.sortResource();
    $scope.refreshFeeds();
  }
  $scope.removeAlbum = function(index){
    // console.log("removed album");
    $scope.socialResource.albums.splice(index, 1);
    $scope.sortResource();
    $scope.refreshFeeds();
  }
  $scope.prev = function(){
    $scope.feedStart -= 5;
    if ($scope.feedStart <0) {
      $scope.feedStart = 0;
    }
    $scope.sortResource();
    $scope.refreshFeeds();
  };
  $scope.next = function(){
    // console.log("next clicked");
    $scope.getFiveStatus = 0;
    $scope.getFive('post');
    $scope.getFive('album');
    $scope.feedStart += 5;
    if ($scope.feedStart > $scope.sortedResourceFeeds.length ) {
      $scope.feedStart -= 5;
    }
  }
  $scope.removeFromTempAlbum = function(index){
    pic = $scope.droppedObjects[index];
    $scope.droppedObjects.splice(index , 1);
    $scope.editorData.draggableObjects.push(pic);
  }
  $scope.createAlbum = function(){
    if ($scope.droppedObjects.length == 0) {
      Flash.create('danger', 'No photos in the album' );
      return;
    }
    for (var i = 0; i < $scope.droppedObjects.length; i++) {
      uri = $scope.droppedObjects[i].url.split('/?')[0];
      // nested request is not supported by the django rest framework so sending the PKs of the photos to the create function in the serializer
      pk = uri.split('picture/')[1];
      $scope.tempAlbum.photos.push(pk);
    }
    dataToPost = {
      user : $scope.me.url,
      title : $scope.tempAlbum.title,
      photos : $scope.tempAlbum.photos,
      tagged : $scope.tempAlbum.tagged,
    };
    // console.log(dataToPost);
    $http({method: 'POST' , data : dataToPost , url : '/api/social/album/'}).
    then(function(response){
      Flash.create('success', response.status + ' : ' + response.statusText );
      $scope.tempAlbum.title = '';
      $scope.tempAlbum.tagged = '';
      $scope.tempAlbum.photos = [];
      $scope.droppedObjects = [];
      $scope.socialResource.albums.push(response.data);
      $scope.sortResource();
      $scope.refreshFeeds();
    }, function(response){
      Flash.create('danger', response.status + ' : ' + response.statusText );
    });
  }
  $scope.onDropComplete=function(data,evt){
    var index = $scope.droppedObjects.indexOf(data);
    if (index == -1){
      $scope.droppedObjects.push(data);
      var index = $scope.editorData.draggableObjects.indexOf(data);
      $scope.editorData.draggableObjects.splice(index , 1);
    }
  }


  var f = new File([""], "");
  $scope.post = {attachment : f , text: ''};
  $scope.publishPost = function(){
    var fd = new FormData();
    fd.append('attachment', $scope.post.attachment);
    fd.append('text' , $scope.post.text );
    fd.append('user' , $scope.me.url);
    if ( typeof $scope.post.tagged !='undefined' && $scope.post.tagged != '' ) {
      fd.append('tagged' , $scope.post.tagged)
    }
    var uploadUrl = "/api/social/post/";
    $http({method : 'POST' , url : uploadUrl, data : fd , transformRequest: angular.identity, headers: {'Content-Type': undefined}}).
    then(function(response){
      $scope.socialResource.posts.push(response.data);
      $scope.sortResource();
      $scope.refreshFeeds();
      $scope.post.attachment = emptyFile;
      $scope.post.text = '';
      $scope.post.tagged = '';
      Flash.create('success', response.status + ' : ' + response.statusText );
    }, function(response){
      Flash.create('danger', response.status + ' : ' + response.statusText );
    });
  };
  $scope.uploadImage = function(){
    var fd = new FormData();
    fd.append('photo', $scope.picturePost.photo);
    fd.append('tagged' , $scope.picturePost.tagged.split(','));
    fd.append('user' , $scope.me.url);
    var uploadUrl = "/api/social/picture/";
    $http({method : 'POST' , url : uploadUrl, data : fd , transformRequest: angular.identity, headers: {'Content-Type': undefined}}).
    then(function(response){
      Flash.create('success', response.status + ' : ' + response.statusText );
      $scope.user.pictures.push(response.data);
      $scope.picturePost.photo = emptyFile;
      $scope.picturePost.tagged = '';

    }, function(response){
      Flash.create('danger', response.status + ' : ' + response.statusText );
    });
  };
  $scope.saveSocial = function(){
    var fd = new FormData();
    fd.append('status', $scope.user.socialData.status);
    if ($scope.user.socialData.coverPicFile != emptyFile) {
      fd.append('coverPic', $scope.user.socialData.coverPicFile);
    }
    fd.append('aboutMe' , $scope.user.socialData.aboutMe);
    var uploadUrl = $scope.user.social;
    $http({method : 'PATCH' , url : uploadUrl, data : fd , transformRequest: angular.identity, headers: {'Content-Type': undefined}}).
    then(function(response){
      Flash.create('success', response.status + ' : ' + response.statusText );
      $scope.user.socialData.coverPic = response.data.coverPic;
      $scope.user.socialData.coverPicFile = emptyFile;
    }, function(response){
      Flash.create('danger', response.status + ' : ' + response.statusText );
    });
  };
});

app.controller('controller.social', function($scope , $http , $timeout , userProfileService , $aside , $interval , $window , $state) {
  $scope.user = userProfileService.get('mySelf').url.split('users/')[0]+'users/'+$state.params.id+'/';
  if ($state.params.id == '') {
    $scope.user = userProfileService.get('mySelf').url;
  }
});