angular.module('app')
  .factory('Prediction', function($http) {
    const baseUrl = 'http://127.0.0.1:5000/'
    return {
      submit: function(down, ydstogo, ScoreDiff) {
        return $http.post(baseUrl, {down, ydstogo, ScoreDiff}).then(data => {
          return data.data
        })
      }
    }
  })
