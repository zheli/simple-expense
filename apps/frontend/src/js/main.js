/*jslint browser: true*/
/*global $, jQuery, angular*/
angular.module(
    'expense_track.app',
    ['ngResource', 'ui.router', 'ngGrid', 'ui.bootstrap', 'ngBootstrap', 'nvd3ChartDirectives']
    )
    .run(
        ['$rootScope','$state','$stateParams',
            function($rootScope, $state, $stateParams) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
            }
        ]
    )
    .config(['$provide', '$httpProvider', function($provide, $httpProvider) {
        $provide.decorator('$resource', function($delegate) {
            return function() {
                if (arguments.length > 0) {  // URL
                    arguments[0] = arguments[0].replace(/\/$/, '\\/');// jshint ignore:line
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
    }]);
