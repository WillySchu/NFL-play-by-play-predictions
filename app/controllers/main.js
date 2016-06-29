angular.module('app')
  .controller('Main', Main)

Main.$inject = ['Prediction', '$state']

function Main(Prediction, $state) {
  const vm = this;

  vm.submit = function(down, ydstogo, ScoreDiff) {
    Prediction.submit(down, ydstogo, ScoreDiff).then(result => {
      vm.result = result;
      $state.go('main.result');
    })
  }
}
