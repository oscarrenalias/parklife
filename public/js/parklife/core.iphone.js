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

$(document).ready(function(){
	$("page_wrapper").css("visibility", "visible");	
	window.scrollTo(0, 1); // pan to the bottom, hides the location bar  	
});