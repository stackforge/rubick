'use strict';


// Declare app level module which depends on filters, and services
angular.module('rubick', [
  'ngRoute',
  'rubick.filters',
  'rubick.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {templateUrl: '/static/partials/main.html', controller: 'ValidateCtrl'});
  $routeProvider.otherwise({redirectTo: '/'});
}]);
