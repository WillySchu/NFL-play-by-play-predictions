angular.module('app')
  .factory('Todos', function($http) {
    const baseUrl = 'http://127.0.0.1:5000/'
    return {
      todos: function() {
        console.log(1);
        return $http.get(baseUrl).then(data => {
          return data;
        })
      },
      todo: function(id) {
        return $http.get(baseUrl + id).then(data => {
          return data;
        })
      }
    }
  })
