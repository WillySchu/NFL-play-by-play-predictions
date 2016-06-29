angular.module('app')
  .config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/')

    $stateProvider
      .state('main', {
        url: '/',
        views: {
          'nav': {
            templateUrl: 'partials/nav.html',
            controller: 'Nav',
            controllerAs: 'nav'
          },
          'content': {
            templateUrl: 'partials/main.html',
            controller: 'Main',
            controllerAs: 'main'
          }
        }
      })
      .state('main.result', {
        url: 'result',
        views: {
          'result@main': {
            templateUrl: 'partials/result.html'
          }
        }
      })
  })
