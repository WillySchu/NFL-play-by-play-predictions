angular.module('app')
  .controller('Nav', Nav)

Nav.$inject = [];

function Nav() {
  const vm = this;

  vm.signIn = function() {
    console.log('Sign In!');
  }
}
