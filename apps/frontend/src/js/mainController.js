angular.module('expense_track.app').
controller('mainController', function($scope, api, authState){
    $scope.list = function(){
        api.expenses.list(function(data){
            $scope.expenses = data;
        });
    };

    $scope.setDateTime= function() {
        $scope.expense.date = new Date();
        $scope.expense.time = $scope.expense.date;
    };


    $scope.datePickerOpen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.datePickerOpened = true;
    };

    $scope.stripDate = function(d) {
        //getMonth() range: 0~11
        return (d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate());
    };

    $scope.stripTime = function(d) {
        return (d.getHours()+":"+d.getMinutes()+":"+d.getSeconds());
    };

    $scope.init = function() {
        $scope.expense = {};
        $scope.setDateTime();
        $scope.authState = authState;
        $scope.list();
        $scope.initdate = new Date();
        $scope.gridOptions = {
            data: 'expenses',
            enableCellSelection: true,
            enableRowSelection: false,
            enableCellEditOnFocus: true,
            columnDefs: [
                {
                    field: '',
                    cellTemplate: '<button type="button" class="btn btn-default btn-sm" ng-click="delete(row)"><i class="glyphicon glyphicon-trash"></i></button>', width:'40',
                    enableCellEdit: false
                },
                {field:'id', displayName:'Id', width:'25'},
                {field:'date', displayName:'Date'},
                {field:'time', displayName:'Time'},
                {field:'amount', displayName:'Amount'},
                {field:'description', displayName:'Description'},
                {field:'comment', displayName:'Comment', width:'**'}
            ]
        };
        $scope.$on('ngGridEventEndCellEdit', function(evt){
                var obj = evt.targetScope.row.entity;
                $scope.update(obj);
        });

    };
    $scope.init();

    $scope.create = function(){
        api.expenses.create({
            date: $scope.stripDate($scope.expense.date),
            time: $scope.stripTime($scope.expense.time),
            amount: $scope.expense.amount,
            description: $scope.expense.description,
            comment: $scope.expense.comment
        });
        $scope.list();
        $scope.expense.amount = '';
        $scope.expense.description = '';
        $scope.expense.comment = '';
    };

    $scope.update = function(obj) {
            api.expenses.update({
                expenseId:obj.id
            }, {
                pub_date:obj.pub_date,
                description:obj.description,
                amount:obj.amount,
                comment:obj.comment
            });
    };

    $scope.delete = function(row){
        var id = row.entity.id;
        api.expenses.delete({expenseId: id}, function(){
            $scope.list();
        });
    };

    $scope.applyDateRange = function(){
        api.expenses.list(
            {
                start_date: $scope.dateRange.startDate.format('YYYY-MM-DD'),
                end_date: $scope.dateRange.endDate.format('YYYY-MM-DD'),
            }, function(data){
            $scope.expenses = data;
        });
    };

    $scope.clearDateRange = function(){
        $scope.dateRange.startDate = new Date();
        $scope.dateRange.endDate = new Date();
        $scope.list();
    };

});
