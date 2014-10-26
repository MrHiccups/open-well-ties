'use strict';

describe('wellTieController', function() {
	beforeEach(module('wellTieApp'));

	var controller, scope;

	beforeEach(inject(function($rootScope, $controller) {
		scope = $rootScope.$new();
		controller = $controller('wellTieController', {$scope: scope});
	}));

	it('should initialise the x and y positions', function() {
		expect(scope.x_position).toBe(0);
		expect(scope.y_position).toBe(0);
	});
});
