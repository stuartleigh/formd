window.formd = (function(formd) {

	"use strict";

	var heroBanner = function() {
		$(document).ready(function(){
			var $hero_content = $('.hero_content').css({
				'perspective': '50px',
				'transform-origin': '50% 50%',
				'position': 'relative'
			});
			var hero_height = $hero_content.outerHeight();
			var hero_bottom = $hero_content.offset().top + hero_height;

			var header_height = $('#nav').outerHeight();
			var cutoff_point = hero_bottom - header_height;

			var scrollPoint, angle, top;

			$(window).on('scroll', function(event) {

				scrollPoint = cutoff_point - $(this).scrollTop();

				angle = 90 - ((scrollPoint / hero_height) * 90);
				angle = Math.max(angle, 0);

				top = 140 - ((scrollPoint / hero_height) * 120);
				top = Math.max(top, 0);

				if(scrollPoint > 0) {
					$hero_content.css({
						'transform': 'rotateX('+angle+'deg)',
						'opacity': (scrollPoint / 100),
						'top': top
					});
				}
			});
		});
	}

	formd.heroBanner = heroBanner;

	return formd

})(window.formd || {});