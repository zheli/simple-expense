angular.module('expense_track.app')
    .factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            var headers = headersGetter();
            headers.Authorization = ('Basic ' + btoa(data.username +
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
                detail: {method: 'GET', url: '/api/v1/expenses/:id/'},
                delete: {method: 'DELETE', url: '/api/v1/expenses/:expenseId/'},
                update: {method: 'PUT', url: 'api/v1/expenses/:expenseId/', params: {expenseId:'@id'}}
            }),
            stats: $resource('/api/v1/statistics/', {}, {
                list: {method: 'GET', isArray: true}
            })
        };
    });
