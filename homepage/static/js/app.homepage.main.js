
app.controller('main' , function($scope , $state , $http , $timeout , $interval){
  console.log("main loded");
  $scope.crmBannerID = 1;

  $scope.mainBannerImages = ['/static/images/main_banner.svg' ]
  $scope.bannerID = 0;

  $scope.typings = ["Realtime inventory" , "Simple and to the point" , "Amazon, Snapdeal , Flipkart integrated" ]

  $scope.typeIndex = 0;


  $interval(function() {

    $scope.typeIndex += 1;
    if ($scope.typeIndex == $scope.typings.length) {
      $scope.typeIndex = 0;
    }

  }, 5000)

  $interval(function() {
    $scope.bannerID += 1;
    if ($scope.bannerID==$scope.mainBannerImages.length) {
      $scope.bannerID = 0;
    }
  } , 2000)

  $interval(function() {
    $scope.crmBannerID += 1;
    if ($scope.crmBannerID==12) {
      $scope.crmBannerID = 1;
    }
  } , 1000)



});
