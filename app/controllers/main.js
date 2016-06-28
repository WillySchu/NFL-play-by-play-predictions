angular.module('app')
  .controller('Main', Main)

Main.$inject = ['Todos']

function Main(Todos) {
  const vm = this;

  vm.todos = function() {
    console.log('0');
    Todos.todos().then(data => {
      console.log(data);
    })
  }
}
