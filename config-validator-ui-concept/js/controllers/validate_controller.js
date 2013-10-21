
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
        $('#add-cluster-modal').modal();
        $('#add-cluster-modal').modal('show');
    }

    $scope.fetchClusters = function() {
        $http.get('/clusters').success(function(data) {
            $scope.clusters = data;
        });
    }

    $scope.fetchClusters();

    $scope.fetchRules = function() {
        $http.get('/rules').success(function(data) {
            $scope.rules = data;
        });
    }

    $scope.fetchRules();


    $scope.addCluster = function() {
        $http.post('/clusters', $scope.newCluster).success(function() {
            $scope.clusters.push($scope.newCluster);
        });
        $scope.newCluster = undefined;
        $('#add-cluster-modal').modal('hide');
    }

    $scope.selectedCluster = undefined;

    $scope.selectCluster = function(clusterId) {
        $scope.selectedCluster = _.find($scope.clusters, function(c) {
            return c.id == clusterId;
        });
    }

    $scope.removeCluster = function(clusterId) {
        $('#remove-cluster-confirm-modal').modal();
        $('#remove-cluster-confirm-modal').modal('show');

        $scope.clusterIdToRemove = clusterId;
    }

    $scope.removeConfirm = function() {
        var url = '/clusters/' + $scope.clusterIdToRemove;
        $scope.clusterIdToRemove = undefined;
        console.log(url);

        $http.delete(url).success(function() {
            $scope.fetchClusters();
            $('#remove-cluster-confirm-modal').modal('hide');
        }).error(function() {
            $('#remove-cluster-confirm-modal').modal('hide');
        });
    }
}])
