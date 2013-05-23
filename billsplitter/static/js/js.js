$(document).ready(function(){
	//Adds a tooltip on small buttons
	$('.btn-small[title]').tooltip();

	//Numeric field
	$('#id_amount').numeric();
});