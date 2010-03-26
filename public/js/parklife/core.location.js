parklife.location = Object();

$(document).ready(function() {
	if( navigator.geolocation ) {
		$('#location_update_button').toggle();
	}
	
	$('#use_location_data').click(function() {
		$('#location_data_controls').toggle();
		parklife.location.showMap(null);
		$('#use_location_data').toggle();
	});	
	
	$('#location_update_button').click(function() { 
		$(this).toggle();
		$(this).parent().append('<img src="/images/spinner.gif" class="spinner" />');
		navigator.geolocation.getCurrentPosition(parklife.callbacks.updateLocation)
	});	
	
	// if the latitude and longitude fields have some data, show the map right away
	if($('#id_lat').val() != "" || $('#id_lng').val() != "" ) {
		$('#location_data_controls').toggle();
		parklife.location.showMap({ lat: $('#id_lat').val(), lng: $('#id_lng').val()});	
		$('#use_location_data').toggle();
	}
});

parklife.callbacks.updateLocation = function(loc)
{
	// update the latitude and longitude fields 
	$('#id_lat').val(loc.coords.latitude);
	$('#id_lng').val(loc.coords.longitude);
	// if we have a location, we can now show it on the map
	latlng = GLatLng(loc.coords.latitude, loc.coords.longitude);
	parklife.location.map._marker.setLatLng(latlng);
	parklife.location.map.panTo(latlng);
	// hide the spinner and show the button to update the location again
	$('#location_update_button').toggle();
	$('#location_update_button').parent().children('.spinner').remove();
}

parklife.location.showMap = function(coords)
{
	// create and display the map
	mapDiv = document.getElementById('map-container');
	parklife.location.map = new GMap2(mapDiv);
	
	if( coords )
		point = new GLatLng(coords.lat, coords.lng);
	else
		point = new GLatLng(41.387885,2.1698);
		
	parklife.location.map.setCenter(point, 13);
  	parklife.location.map.setUIToDefault();
	// add the marker
	marker = new GMarker(point, {draggable: true, bouncy: true});
	GEvent.addListener(marker, "dragend", function(latlng) {
		// update the latitude and longitude fields in the form
		$('#id_lat').val(latlng.lat());
		$('#id_lng').val(latlng.lng());			
	});
	parklife.location.map._marker = marker;
	parklife.location.map.addOverlay(marker);
}