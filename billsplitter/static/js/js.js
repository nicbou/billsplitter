$(document).ready(function(){
	//Adds a tooltip on small buttons
	$('.btn-small[title]').tooltip();

	//Numeric field
	$('#id_amount').numeric();

	//Parallax on home page
	var scrollPos;
	var header = $('.jumbotron')
	var header_static = $('.jumbotron h1')
	$(window).scroll(function () {
		//Position in the page
		scrollPos = jQuery(this).scrollTop();

		//Scroll the banner text
		header.css({
			'background-position': "left " + (scrollPos * -0.5 - 100) + "px",
		});
		header_static.css({
			'top': (scrollPos * -0.5 + 520) + "px",
		})
	});
});