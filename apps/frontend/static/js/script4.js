angular.module('expense_track.app', ['ngResource', 'ui.router', 'ngGrid']).
    config(function($stateProvider, $urlRouterProvider){
        $urlRouterProvider.otherwise("/list");
        $stateProvider.
        state('list', {
             url: "/list",
             controller: "listController",
             templateUrl: "static/partials/expense.list.html"
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
    config(['$provide', '$httpProvider', function($provide, $httpProvider) {
        $provide.decorator('$resource', function($delegate) {
            return function() {
                if (arguments.length > 0) {  // URL
                    arguments[0] = arguments[0].replace(/\/$/, '\\/');
                }
                if (arguments.length > 2) {  // Actions
                    angular.forEach(arguments[2], function(action) {
                        if (action && action.url) {
                            action.url = action.url.replace(/\/$/, '\\/');
                        }
                    });
                }
                return $delegate.apply($delegate, arguments);
            };
        });
        $provide.factory('resourceEnforceSlashInterceptor', function() {
            return {
                request: function(config) {
                    config.url = config.url.replace(/[\/\\]+$/, '/');
                    return config;
                }
            };
        });
        $httpProvider.interceptors.push('resourceEnforceSlashInterceptor');
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }]).
    service('authState', function () {
        return {
            user: undefined
        };
    }).
    factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        return {
            auth: $resource('/api/v1/auth/', {}, {
                login:  {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('/api/v1/users/', {}, {
                create: {method: 'POST'}
            }, false),
            expenses: $resource('/api/v1/expenses/', {}, {
                list:   {method: 'GET', isArray: true},
                create: {method: 'POST'},
                detail: {method: 'GET', url: '/api/v1/expenses/:id'},
                delete: {method: 'DELETE', url: '/api/v1/expenses/:id'}
            })
        };
    }).
    controller('authController', function($scope, api, authState) {
        $('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.authState = authState;

        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
        $scope.login = function(){
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        authState.user = data.username;
                    }).
                    catch(function(data){
                        alert(data.data.detail);
                    });
        };
        $scope.logout = function(){
            api.auth.logout(function(){
                authState.user = undefined;
            });
        };
        $scope.register = function($event){
            $event.preventDefault();
            api.users.create($scope.getCredentials()).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
        };
    }).
    controller('listController', function($scope, api, authState){
        $scope.authState = authState;
        $scope.list = function(){
            api.expenses.list(function(data){
                $scope.expenses = data;
            });
        };
        $scope.list();
    }).
    controller('expenseController', function($scope, api, authState){

        $scope.authState = authState;
        $scope.myData = [{name: "Moroni", age: 50},
                         {name: "Tiancum", age: 43},
                         {name: "Jacob", age: 27},
                         {name: "Nephi", age: 29},
                         {name: "Enos", age: 34}];
        //$scope.gridOptions = { data: 'myData'  };

        $scope.list = function(){
            api.expenses.list(function(data){
                $scope.expenses = data;
            });
        };
        $scope.list();
        $scope.gridOptions = {
            data: 'expenses',
            enableCellSelection: true,
            enableRowSelection: false,
            enableCellEditOnFocus: true,
            columnDefs: [
                {field:'id', displayName:'Id'},
                {field:'amount', displayName:'Amount'},
                {field:'description', displayName:'Description'},
                {field:'id', displayName:'', cellTemplate: '<div>Edit</div>'}
            ]
        };

        $scope.create = function(){
            var data = {body: $scope.body};
            api.expenses.create(data, function(data){
                $scope.body = '';
                $scope.expenses.unshift(data);
            });
        };

        $scope.delete = function(id){
            api.expenses.delete({id: id}, function(){
                $scope.expenses.splice($scope.utils.getExpenseIndex(id), 1);
            });
        };

        $scope.utils = {
            getExpenseIndex: function(id){
                return _.indexOf(
                    $scope.expenses,
                    _.findWhere($scope.expenses, {id: id})
                );
            }
        };
    });
