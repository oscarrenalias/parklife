

parklife.widgets.places = {
	map: null,
	markers: Array(),
	current: 0,
	
	init: function(box) {
				
	    var myOptions = {
	      zoom: 1,
	      center: new google.maps.LatLng(0, 0),
		  mapTypeId: google.maps.MapTypeId.ROADMAP
	    }
	    parklife.widgets.places.map = new google.maps.Map(document.getElementById(box), myOptions);	
		
		$.ajax({
			url:"/places?f=json",
			dataType:"jsonp",
			success:function(data) {
				// create the markers based on the entries received
				for(i in data.entries) {
					e = data.entries[i];
					var latLng = new google.maps.LatLng(e.lat, e.lng);
				    var marker = new google.maps.Marker({
				        position: latLng,
				        map: parklife.widgets.places.map,
				        title:e.title
				    });
					parklife.widgets.places.setInfoWindow(marker, e);
					
					// save a reference to the object
					marker.__index = parseInt(i);
					parklife.widgets.places.markers[i] = marker;
				}
				
				// add the "previous"' and '"next" buttons
				boxId = "#" + box;
				$(boxId).after(
					'<div id="places-marker-buttons">' +
					'<div class="marker-buttons-prev"><a href="#" id="places-prev-link">Previous Place</a></div>' +
					'<div class="marker-buttons-next"><a href="#" id="places-next-link">Next Place</a></div>' +
					'</div>');
				$('#places-prev-link').click(parklife.widgets.places.prevMarker);
				$('#places-next-link').click(parklife.widgets.places.nextMarker);
			}		
		});		
	},
	
	setInfoWindow: function(marker, entry) {
		// we need to handle blog entries a little differently from other entries
		if(entry.source == "blog")
			var content = '<b><a href="' + e.permalink + '">' + e.title + '</a></b><br/>' + e.text;
		else
			var content = '<b><a href="' + e.permalink + '">' + e.text + '</a></b>';
			
		// we attach the infowindow to the marker so that we can easily find it later
		marker.__infoWindow = new google.maps.InfoWindow({ 
				content: content,
				maxWidth: 500
		});
		google.maps.event.addListener(marker, 'click', function() {
			parklife.widgets.places.current = marker.__index;
			// increase the zoom if it's very small, otherwise we can't see anything...
			if(parklife.widgets.places.map.getZoom() < 2)
				parklife.widgets.places.map.setZoom(8);
			marker.__infoWindow.open(parklife.widgets.places.map,marker);
		});
	},
	
	nextMarker: function() {
		parklife.widgets.places.closeCurrentMarker();		
		parklife.widgets.places.current = (parklife.widgets.places.current + 1) % parklife.widgets.places.markers.length;
		parklife.widgets.places.showCurrentMarker();
	},
	
	prevMarker: function() {
		parklife.widgets.places.closeCurrentMarker();		
		parklife.widgets.places.current = (parklife.widgets.places.current - 1) % parklife.widgets.places.markers.length;
		if( parklife.widgets.places.current < 0 )
			parklife.widgets.places.current = parklife.widgets.places.markers.length-1;
		parklife.widgets.places.showCurrentMarker();		
	},
	
	showCurrentMarker: function() {
		parklife.widgets.places.showMarker(parklife.widgets.places.markers[parklife.widgets.places.current]);
	},
	
	closeCurrentMarker: function() {
		parklife.widgets.places.markers[parklife.widgets.places.current].__infoWindow.close();
	},
		
	showMarker: function(marker) {		
		parklife.widgets.places.map.panTo(marker.getPosition());
		google.maps.event.trigger(marker, 'click');
	}
};