'use strict';

angular.module('cartrips', ['ngRoute', 'ngCookies', 'cartripsDirectives', 'cartripsServices', 'http-auth-interceptor'])

.config(function($routeProvider, $locationProvider, $httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
 
  $routeProvider
    .when('/trips', {
      controller:'ListCtrl',
      templateUrl:'/static/list.html'
    })
    .when('/trips/edit/:projectId', {
      controller:'EditCtrl',
      templateUrl:'/static/detail.html'
    })
    .when('/trips/new', {
      controller:'CreateCtrl',
      templateUrl:'/static/detail.html'
    })
    .when('/', {
      conroller:'Welcome',
      templateUrl:'/static/home.html'
    })
    .otherwise({
      redirectTo:'/'
    });

  $locationProvider.html5Mode(true);
});
