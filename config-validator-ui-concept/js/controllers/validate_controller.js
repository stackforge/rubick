
/* Controllers */

angular.module('rubick.controllers', []).
    controller('ValidateCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
    $scope.currentStep = "cluster";
    $scope.ruleGroup = "valid";

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
            $scope.fetchClusters();
            $scope.newCluster = undefined;
            $('#add-cluster-modal').modal('hide');
            $scope.$apply();
        });
    }

    $scope.selectedCluster = undefined;

    $scope.selectCluster = function(clusterId) {
        $scope.selectedCluster = _.find($scope.clusters, function(c) {
            return c.id == clusterId;
        });

        $scope.diagnosticsFinished = false;
    }

    $scope.removeCluster = function(clusterId) {
        $('#remove-cluster-confirm-modal').modal();
        $('#remove-cluster-confirm-modal').modal('show');

        $scope.clusterIdToRemove = clusterId;
    }

    $scope.removeConfirm = function() {
        var url = '/clusters/' + $scope.clusterIdToRemove;
        $scope.clusterIdToRemove = undefined;

        $http.delete(url).success(function() {
            $scope.fetchClusters();
            $('#remove-cluster-confirm-modal').modal('hide');
        }).error(function() {
            $('#remove-cluster-confirm-modal').modal('hide');
        });
    }

    $scope.runValidation = function() {
        var postData = { cluster_id: $scope.selectedCluster.id }

        $http.post('/validation', postData).success(function(job) {
            $scope.currentJobId = job.id;

            var poll = function() {
                $timeout(function() {
                    $http.get('/validation/' + $scope.currentJobId).success(function(jobData) {
                        console.log(jobData);
                        switch (jobData.state) {
                            case "success":
                                $scope.results = jobData.result;
                                $scope.diagnosticsFinished = true;
                                break;
                            case "failure":
                                $scope.jobError = jobData.message;
                                break;
                            default:
                                poll();
                                break;
                        }
                    });
                }, 2000);
            };     
            poll();

        });

        //$http.get('/static/data/validate_stub.json').success(function(data) {
            //$scope.results = data;
        //});
    }

    //$scope.componentFilter = false;

    $scope.toggleEmptyComponents = function(component) {
        return !$scope.componentFilter || component.issues;
    }
}])
