function ValidatorCtrl($scope) {
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

    $scope.clusters = [
        {
            name: "Kirill's DevStack",
            description: "Grizzly-based devstack with Quantum and oVS, deployed on Kirill's laptop",
            sshKey: "beasdfahsldjhfsadg",
            nodesCount: 2,
            status: "Available",
            lastChecked: moment().startOf('hour').fromNow()
        },
        {
            name: "Peter's DevStack",
            description: "Grizzly-based devstack deployed on Peter Lomakin's workstation with nova-network and FlatDHCP manager",
            sshKey: "beasdfahsldjhfsadg",
            nodesCount: 5,
            status: "Broken",
            lastChecked: moment().startOf('day').fromNow()
        }
    ]

    $scope.addCluster = function() {
        $scope.newCluster.nodesCount = 20;
        $scope.newCluster.status = "Available";
        $scope.clusters.push($scope.newCluster);
        $scope.newCluster = undefined;
        $('#add-cluster-modal').modal('hide');
    }

}
