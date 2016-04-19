app.config(function($stateProvider){

  $stateProvider
  .state('projectManagement.GIT', {
    url: "/GIT",
    views: {
       "": {
          templateUrl: '/static/ngTemplates/app.GIT.html',
       },
       "menu@projectManagement.GIT": {
          templateUrl: '/static/ngTemplates/app.GIT.menu.html',
          controller : 'projectManagement.GIT.menu',
        },
        "@projectManagement.GIT": {
          templateUrl: '/static/ngTemplates/app.GIT.default.html',
          controller : 'projectManagement.GIT.default',
        }
    }
  })
  .state('projectManagement.GIT.groups', {
    url: "/groups",
    templateUrl: '/static/ngTemplates/app.GIT.groups.html',
    controller: 'projectManagement.GIT.groups'
  })
  .state('projectManagement.GIT.repos', {
    url: "/repos",
    templateUrl: '/static/ngTemplates/app.GIT.repos.html',
    controller: 'projectManagement.GIT.repos'
  })
  .state('projectManagement.GIT.manage', {
    url: "/manage",
    templateUrl: '/static/ngTemplates/app.GIT.manage.html',
    controller: 'projectManagement.GIT.manage'
  })

});

app.controller('projectManagement.GIT.default' , function($scope , $http , $aside , $state, Flash , $users , $filter , $permissions){
  $scope.page = 0;

  $scope.fetchNotifications = function() {
    $http({method : 'GET' , url : '/api/git/commitNotification/?limit=10&offset=' + $scope.page * 10}).
    then(function(response) {
      $scope.count = response.data.count;
      $scope.notifications = response.data.results;
      var d = new Date($scope.notifications[0].time);
      $scope.notifications[0].dateShow = true;
      $scope.notifications[0].time = d;
      for (var i = 1; i < $scope.notifications.length; i++) {
        var d2 = new Date($scope.notifications[i].time);
        $scope.notifications[i].time = d;
        if (d.getMonth()!= d2.getMonth() || d.getFullYear() != d2.getFullYear() ) {
          $scope.notifications[i].showDate = true;
          d = d2;
        }else {
          $scope.notifications[i].showDate = false;
        }
      }
    });
  }

  $scope.nextPage = function() {
    $scope.page += 1;
    $scope.fetchNotifications()
  }
  $scope.prevPage = function() {
    $scope.page -= 1;
    if ($scope.page < 0) {
      $scope.page += 1;
    }
    $scope.fetchNotifications()
  };

  $scope.fetchNotifications()


});

app.controller('projectManagement.GIT.menu' , function($scope , $http , $aside , $state, Flash , $users , $filter , $permissions){
  // settings main page controller

  var getState = function(input){
    parts = input.name.split('.');
    // console.log(parts);
    return input.name.replace('app' , 'projectManagement')
  }

  $scope.apps = [];

  $scope.buildMenu = function(apps){
    for (var i = 0; i < apps.length; i++) {
      a = apps[i];
      parts = a.name.split('.');
      if (a.module != 10 || parts.length != 3 || parts[1] != 'GIT') {
        continue;
      }
      a.state = getState(a)
      a.dispName = parts[parts.length -1];
      $scope.apps.push(a);
    }
  }

  as = $permissions.app();
  if(typeof as.success == 'undefined'){
    $scope.buildMenu(as);
  } else {
    as.success(function(response){
      $scope.buildMenu(response);
    });
  };

  $scope.isActive = function(index){
    app = $scope.apps[index]
    if (angular.isDefined($state.params.app)) {
      return $state.params.app == app.name.split('.')[2]
    } else {
      return  $state.is(app.name.replace('app' , 'projectManagement'))
    }
  }

});