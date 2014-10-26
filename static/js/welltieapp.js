'use strict';

var wellTieApp = angular.module('wellTieApp', ['ui.slider']);

wellTieApp.controller('wellTieController', function ($scope) {
	$scope.position = {x:0, y:0};

	var loadImage = function(class_name,url) {
					var element_to_replace = $('.' + class_name);
					element_to_replace.attr('src','/static/img/busy.gif');

					var image = new Image();

					image.onload = function() {
						element_to_replace.replaceWith(image);
						$(image).attr('class', element_to_replace.attr('class'));
					};

				image.src = url;
			};


	var requestReflectivity = function() {
		loadImage('reflectivity-graph', '/plot?type=reflectivity&shift=' + $scope.position.x);	
	};

	$scope.$watch('position.x', function(newValue, oldValue) {
		requestReflectivity();
	});

	
	loadImage('spectrum-graph', '/plot?type=spectrum');


});
