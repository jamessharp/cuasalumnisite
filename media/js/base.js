$(document).ready(function(){
	// Set datepicker on the dateField classes.
	$('.dateField').datepicker();
	
	// Set visibility on any required fields
	$('#tr_service_joined').hide();
	$('#tr_service_joined_details').hide();
	$('#tr_service_rank').hide();
	
	$('#id_joined_service').change(function(){
		$('#tr_service_joined').toggle();
		$('#tr_service_joined_details').toggle();
		$('#tr_service_rank').toggle();
	});

});
