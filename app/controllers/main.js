angular.module('app')
  .controller('Main', Main)

Main.$inject = ['Todos']

function Main(Todos) {
  const vm = this;

  vm.todos = function() {
    Todos.todos().then(data => {
      console.log(data);
    })
  }

  vm.submit = function() {
    console.log('submit');
  }
}
