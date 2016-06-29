angular.module('app')
  .controller('Main', Main)

Main.$inject = ['Prediction']

function Main(Prediction) {
  const vm = this;

  vm.submit = function(down, ydstogo, ScoreDiff) {
    Prediction.submit(down, ydstogo, ScoreDiff)
  }
}
