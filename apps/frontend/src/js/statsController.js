angular.module('expense_track.app')
.controller('statsController', function($scope, api, authState) {
    $scope.stats = {};
    $scope.year_list = [];
    $scope.yFunction = function(){
        return function(d){
            return d[1];
        };
    };
    $scope.fetch = function(year) {
        var api_params = {};
        if (year!='all') {
            api_params = {
                year: year
            };
        }
        api.stats.list(api_params, function(data){
            week_total_spending_data = {"key":"Weekly Total Spending", "values":[]};
            average_day_spending_data = {"key":"Average Day Spending", "values":[]};
            for (i=0;i<data.length;i++) {
                week_total_spending_data.values.push([data[i].week_number, data[i].total_spending]);
                average_day_spending_data.values.push([data[i].week_number, data[i].average_day_spending]);
                if ($scope.year_list.indexOf(data[i].year) == -1) {
                    $scope.year_list.push(data[i].year);
                }
            }
            $scope.stats.total = [];
            $scope.stats.average = [];
            $scope.stats.total.push(week_total_spending_data);
            $scope.stats.average.push(average_day_spending_data);
        });
    };

    $scope.selectedYear = new Date();
    $scope.selectedYear = $scope.selectedYear.getFullYear();

    $scope.fetch('all');
});
