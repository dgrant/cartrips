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
  $http.get('http://localhost:5000/api/trips').
    success(function(data) {
        $scope.trips = data.trips;
    });
}
