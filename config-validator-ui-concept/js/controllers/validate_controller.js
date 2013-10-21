
/* Controllers */

angular.module('rubick.controllers', []).
    controller('ValidateCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.currentStep = "cluster";
    $scope.ruleGroup = "valid";
    $scope.ipPattern = 

    $scope.setStep = function(step) {
        $scope.currentStep = step;
    }

    $scope.setRuleGroup = function(group) {
        $scope.ruleGroup = group;
    }

    $('.ui.accordion').accordion();

    $scope.getAddClusterFormErrors = function() {
        var errors = []
        var required = $scope.addClusterForm.$error.required;
        var pattern = $scope.addClusterForm.$error.pattern;

        if (required) {
            _.each(required, function(e) {
                switch (e.$name) {
                    case 'name':
                        errors.push("Cluster name cannot be empty.");
                    break;
                    case 'private_key':
                        errors.push("SSH Key is missing.");
                    break;
                    default:
                        break;
                }
            });
        }

        if (pattern) {
            errors.push("Invalid IP address.");
        }

        return errors;
    }

    $scope.getErrorClass = function(fieldName, collection) {
        if (collection) {
            return _.find(collection, function(e) {
                return e.$name == fieldName;
            });
        } else {
            return false;
        }
    }

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
        $http.post('/clusters', $scope.newCluster).success(function() {
            $scope.clusters.push($scope.newCluster);
        });
        $scope.newCluster = undefined;
        $('#add-cluster-modal').modal('hide');
    }

    $scope.selectedCluster = undefined;

    $scope.selectCluster = function(clusterId) {
        console.log(clusterId);
        $scope.selectedCluster = _.find($scope.clusters, function(c) {
            return c.id == clusterId;
        });
        console.log($scope.seletedCluster);
    }
}])
