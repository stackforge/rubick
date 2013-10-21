'use strict';

/* Filters */

angular.module('rubick.filters', []).
    filter('colorizeIssue', [function() {
    return function(text) {
        var error='<div class="ui red horizontal label">Error</div>';
        return String(text).replace('[ERROR]', error);
    }
}]);
