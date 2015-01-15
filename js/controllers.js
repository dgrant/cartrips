"use strict";

function CredentialsController($scope, loginService) {
    $scope.credentials = { userName: '', password: '' };
    
    $scope.submit = function() {
        loginService.setUserNameAndPassword($scope.credentials.userName, $scope.credentials.password);
    }
}

function LoginController($scope, $location, loginService) {
    $scope.isLoggedIn = function() {
        return loginService.isLoggedIn();
    }
    
    $scope.logOut = function() {
        loginService.logOut();
        $location.path('/about');
    }
}

function ListCtrl($scope, $http) {
  $http.get('http://localhost:5001/api/trips').
    success(function(data) {
        $scope.trips = data.trips;
    });
}

function CreateCtrl($scope, $location, $timeout, $http) {
  $scope.save = function() {
      $http.post('http://localhost:5001/api/trips', $scope.).
        success(function(data) {
            $location.path('/api/trips');
        })};
}
