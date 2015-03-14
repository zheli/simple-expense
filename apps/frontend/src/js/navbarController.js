angular.module('expense_track.app').
controller('navbarController', function($scope, $state, $location){
    $scope.isActive = function (sref) {
        return $state.href(sref) === '#'+$location.path();
    };
});
