parklife.iphone = Object();

parklife.iphone.updateOrientation = function() 
{  
     var contentType = "show_";  
     switch(window.orientation) {  
         case 0:  
         contentType += "normal";  
         break;  
   
         case -90:  
         contentType += "right";  
         break;  
   
         case 90:  
         contentType += "left";  
         break;  
   
         case 180:  
         contentType += "flipped";  
         break;  
     }  

	$("page_wrapper").css("class", contentType);
}

parklife.callbacks.updateLocation = function(loc)
{
	// update the latitude and longitude fields 
	$('#id_lat').val(loc.coords.latitude);
	$('#id_lng').val(loc.coords.longitude);
	$('.spinner').remove();	
	// show a link where the current location can be seen
	$('#see_location').attr('href', 'http://maps.google.com?f=q&amp;source=s_q&amp;geocode=&amp;q=' + loc.coords.latitude + '+' + loc.coords.longitude);
	$('#see_location').show();
}

$(document).ready(function(){
	$("page_wrapper").css("visibility", "visible");	
	window.scrollTo(0, 1); // pan to the bottom, hides the location bar  	
	
	// overwrite the behaviour of this button if we are in an iphone
	$('#location_update_button').unbind("click");
	$('#location_update_button').click(function() { 
		$(this).toggle();
		$(this).parent().append('<img src="/images/spinner.gif" class="spinner" />');
		navigator.geolocation.getCurrentPosition(parklife.callbacks.updateLocation)
	});
	
	// show the location in google maps
	$('#see_location').click(function() {
		return(true);
	});
	
	$('#show_admin_menu').click(function() {
		$('#admin_menu').toggle();
		return(false);	
	});	
});

