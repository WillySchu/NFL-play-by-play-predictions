angular.module('app')
  .factory('Prediction', function($http) {
    const baseUrl = 'http://127.0.0.1:5000/'
    return {
      submit: function(down, ydstogo, ScoreDiff) {
        data = JSON.stringify({down, ydstogo, ScoreDiff});
        console.log(data);
        $http.post(baseUrl, {down, ydstogo, ScoreDiff}).then(data => {
          console.log(data);
        })
      }
    }
  })
