angular.module('expense_track.app')
    .service('authState', function () {
        return {
            user: undefined
        };
    })
    .service('authService', function(authState) {
        return {
            isAuthenticated: function() {
                return !(authState.user === '' || typeof authState.user === 'undefined');
            }
        };
    });
