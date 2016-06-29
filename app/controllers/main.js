angular.module('app')
  .controller('Main', Main)

Main.$inject = ['Prediction', '$state']

function Main(Prediction, $state) {
  const vm = this;

  vm.submit = function(down, ydstogo, ScoreDiff) {
    Prediction.submit(down, ydstogo, ScoreDiff).then(function(result) {
      if (result === 1) {
        vm.result = 'Pass';
      } else if (result === 2) {
        vm.result = 'Run';
      } else {
        vm.result = 'Other';
      }
      $state.go('main.result');
    })
  }
}
