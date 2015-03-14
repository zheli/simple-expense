angular.module('expense_track.app').
    config(function($stateProvider, $urlRouterProvider){
        $urlRouterProvider.otherwise("/readme");
        $stateProvider.
        state('readme', {
            url: "/readme",
            templateUrl: "static/partials/readme.html",
            data: {
                requireAuth: false
            }
        }).
        state('list', {
            url: "/list",
            controller: "mainController",
            templateUrl: "static/partials/expense.list.html",
            data: {requireAuth: true}
        }).
        state('stats', {
            url: "/stats",
            controller: "statsController",
            templateUrl: "static/partials/expense.stats.html",
            data: {requireAuth: true}
        }).
        state('state1', {
            url: "/state1",
            templateUrl: "static/partials/state1.html"
        }).
        state('state1.list', {
            url: "/list",
            templateUrl: "static/partials/state1.list.html",
            controller: function($scope) {
                $scope.items = ["A", "List", "Of", "Items"];
            }
        }).
        state('state2', {
            url: "/state2",
            templateUrl: "static/partials/state2.html"
        }).
        state('state2.list', {
            url: "/list",
            templateUrl: "static/partials/state2.list.html",
            controller: function($scope) {
                $scope.things = ["A", "Set", "Of", "Things"];
            }
        });
    }).
    run(function($rootScope, $state, authService) {
        $rootScope.$on('$stateChangeStart', function(event, next){
            if(next.data.requireAuth) {
                if (!authService.isAuthenticated()) {
                    console.log('User is not logged in.');
                    event.preventDefault();
                    $state.go('readme');
                }
            }
        });
    });
