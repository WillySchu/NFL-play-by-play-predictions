angular.module('app')
  .factory('Prediction', function($http) {
    const baseUrl = 'http://10.5.82.83:5000/'
    return {
      submit: function(down, ydstogo, ScoreDiff) {
        return $http.post(baseUrl, {down, ydstogo, ScoreDiff}).then(function(data) {
          return data.data
        })
      }
    }
  })
