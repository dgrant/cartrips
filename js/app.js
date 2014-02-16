'use strict';

angular.module('cartrips', ['ngRoute', 'ngCookies', 'cartripsDirectives', 'cartripsServices', 'http-auth-interceptor'])

.config(function($routeProvider, $locationProvider, $httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $locationProvider.html5Mode(true).hashPrefix('/static/');
 
  $routeProvider
    .when('/', {
      controller:'ListCtrl',
      templateUrl:'/static/list.html'
    })
    .when('/edit/:projectId', {
      controller:'EditCtrl',
      templateUrl:'/static/detail.html'
    })
    .when('/new', {
      controller:'CreateCtrl',
      templateUrl:'/static/detail.html'
    })
    .otherwise({
      redirectTo:'/'
    });
});
