'use strict';

describe('wellTieController', function() {
	beforeEach(module('wellTieApp'));

	var controller, scope;

	beforeEach(inject(function($rootScope, $controller) {
		scope = $rootScope.$new();
		controller = $controller('PhoneListCtrl', {$scope: scope});
	}));

	it('should initialise the x and y positions', function() {
		expect(scope.x_position, toEqual(0));
		expect(scope.y_position, toEqual(1));
	});
});
