
/* Controllers */

angular.module('rubick.controllers', []).
    controller('ValidateCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.currentStep = "cluster";
    $scope.ruleGroup = "valid";

    $scope.setStep = function(step) {
        $scope.currentStep = step;
    }

    $scope.setRuleGroup = function(group) {
        $scope.ruleGroup = group;
    }

    $('.ui.accordion').accordion();

    $scope.showAddClusterModal = function() {
        $('.ui.modal').modal();
        $('#add-cluster-modal').modal('show');
    }

    $http.get('/clusters').success(function(data) {
        $scope.clusters = data;
    });

    $http.get('/rules').success(function(data) {
        $scope.rules = data;
    });

    $scope.addCluster = function() {
        $scope.newCluster.nodesCount = 20;
        $scope.newCluster.status = "Available";
        $scope.clusters.push($scope.newCluster);
        $scope.newCluster = undefined;
        $('#add-cluster-modal').modal('hide');
    }
}])
