angular.module('app')
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/')

    $stateProvider
      .state('main', {
        url: '/',
        views: {
          'content': {
            templateUrl: 'partials/main.html',
            controller: 'Main',
            controllerAs: 'main'
          }
        }
      })
  })
