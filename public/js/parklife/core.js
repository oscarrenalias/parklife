/**
 * Parklife core javascript functions
 */

parklife = Object();
parklife.config = Object();
parklife.callbacks = Object();
parklife.events = Object();

parklife.updateEntry = function(entry_id)
{
	return(false);	
}

parklife.editEntry = function(entry_id)
{
	$("#item_" + entry_id).html("<textarea class=\"mceEditor\">" + 	$("#item_text_" + entry_id).html() + "</textarea>");
	
	tinyMCE.init({
			theme : "advanced",
			mode : "specific_textareas",
			editor_selector : "mceEditor",
			plugins : "emotions, inlinepopups",
			theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,bullist,numlist,outdent, indent,undo,redo,link,unlink,image, charmap, code",
			theme_advanced_buttons2 : "",
			theme_advanced_buttons3 : "",
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
			extended_valid_elements : "div[id,class,style],iframe[src|width|height|frameborder],object[width|height|type|data],embed[src|type|width|height|wmode|flashvars], param[name|value], a[name|href|target|title|onclick],img[width|class|src|border=0|alt|title|hspace|vspace|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],span[class|align|style], p",
			cleanup: "true",
			convert_urls : false,
			debug : false
	});	
}

parklife.callbacks.deleteEntry = function(o)
{
	if( o.error == false) {
		$('#item_wrapper_' + o.entry_id).hide("puff", "swing", 1000);
	}
	else {
		window.alert(o.message)
		// destroy the spinner
		$("#spinner_" + o.entry_id ).remove();
		// and show the edit controls again
		$("#item_actions_wrapper_" + o.entry_id).show();
	}
	
	return(false);
}

parklife.getSpinnerCode = function(id)
{
	return( "<img src=\"/images/spinner.gif\" class=\"spinner\" id=\"spinner_" + id + "\" />" )
}

parklife.deleteEntry = function(entry_id)
{
	$.Delete('/service/entry/{id}', { id: entry_id }, parklife.callbacks.deleteEntry )
	// show the ajax spinner
	item_actions_div = '#item_actions_' + entry_id;
	item_actions_wrapper_div = '#item_actions_wrapper_' + entry_id;	
	$(item_actions_wrapper_div).hide();
	$(item_actions_div).append(parklife.getSpinnerCode("spinner_" + entry_id));
	
	return(false);
}

/**
 * callback for handling search request responses
 */
parklife.callbacks.googleSearchCallback = function(resp)
{	
	// show the results
	var resultData = '';
	
	if( resp.responseData.results.length > 0 ) {
		$.each(resp.responseData.results, function(i, result) {			
			code = '\
			<div class="search-result-icon"><img class="icon" src="/images/google.png" height="16" width="16"></div>\
			<div class="search-result" id="search-result-' + i + '">\
			<div class="search-result-title"><a href="' + result.url + '">' + result.title + '</a></div>\
			<div class="search-result-content">' + result.content +'</div>\
			</div>\n';
			resultData += code;
		});
	}
	else {
		resultData += 'No results found';
	}
	
	// and show the cursor
	var pagerCode = '';
	if( resp.responseData.cursor.pages != undefined ) {
	  	var cursor = resp.responseData.cursor;
		pagerCode = '<div class="search-results-pager">';
		$.each(cursor.pages, function(i, page) {
	    	if (cursor.currentPageIndex == i) { // if we are on the curPage, then don't make a link
				pagerCode += page.label;
	    	} else {
				pagerCode += '<a href="javascript:parklife.search(' + page.start +')" class="search-cursor-page-link">' + page.label + '</a>';
	    	}
	  	});
		// add a link to the page with more results
		pagerCode += ' › <a href="' + resp.responseData.cursor.moreResultsUrl + ' ">More results</a>';
		pagerCode += '</div>';
	}

  	$('#searchresults').html(resultData + pagerCode );
}

/**
 * Initiates the search process
 * @param start Leave it empty to initiate a search, or pass a start offset to retrieve
 * the results starting at that point
 */	
parklife.search = function(start) 
{
	if( start == undefined ) start = 0;			
	
	terms = $('#searchTerms')[0].value;
		
	$.ajax({
		url: "http://ajax.googleapis.com/ajax/services/search/web",
		data: { "v": "1.0", "q": terms, "cx": parklife.config.GOOGLE_CUSTOM_SEARCH_ENGINE_KEY, "start": start, "rsz": "large", "key": parklife.config.GOOGLE_API_KEY },
		dataType: "jsonp",
		jsonpCallback: "parklife.callbacks.googleSearchCallback",
		success: parklife.callbacks.googleSearchCallback,
		beforeSend: function(req) {
			req.setRequestHeader("Referer", "www.renalias.net" );
		}
	});
}

parklife.showSearch = function()
{
	terms = $('#searchTerms')[0].value;	
	if( terms == "" || terms == undefined )
		return(false);	
	
	// hide the content div and the pager, since we don't need them here
	$('#content').hide();
	$('#pager').hide();	
	// and show the container for the search results
	$('#searchresults-container').show();
	parklife.search();
}

parklife.closeSearch = function()
{
	// show the content div and the pager
	$('#content').show();
	$('#pager').show();	
	// and show the container for the search results
	$('#searchresults-container').hide();
	$('#searchresults').html('');	
}

$(document).ready(function(){
	// set the event handler for the deletion of entries
	$(".delete_entry").each(function(index) {
		$(this).click(function(e) {
			// this has somethingn to do with the event model, but i'm not sure why -
			// sometimes it's the IMG tag, as a child of the anchor tag, the element
			// that generates the event... in that case, we don't have access to the '"rel"
			// attribute so we need to look one level up to find it
			if(e.target.tagName.toLowerCase()=='img') id = e.target.parentNode.rel;
			else id = e.target.rel;
			parklife.deleteEntry(id); 
			return(false) 
		});
	});

	// key handlder for submitting searches via the return key
	$('#searchTerms').keypress(function(event) {
		if(event.keyCode == 13) {
			$('#submitSearchButton').click();
			event.preventDefault();
		}		
	});
	
	// event handler for geotag links 
	$('.geotag-data').click(function(e) {
		
		//hackish, but we don't need someone else's events...
		if(!$(e.target).hasClass('geotag-icon')) {
			e.preventDefault();
			return( false );
		}
		
		if( this['mapAlreadyBuilt'] == true ) {
			mapDiv = $(this).find('.geotag-map-container');
			if($(mapDiv).css("display") == "none" ) {
				// we may need to reposition the map, if for some reason
				// the page scrolled since the last time we showed it
				// but only if the map is currently hidden				
				if((e.clientY + 300) > window.innerHeight) {
					$(mapDiv).css( "top", (Math.round($(this).position()['top']) - (300 + 10)) + 'px');
					$(mapDiv).css( "left", Math.round($(this).position()['left']) + 'px');
				}
				else {
					$(mapDiv).css( "top", (Math.round($(this).position()['top']) + 15) + 'px');
					$(mapDiv).css( "left", Math.round($(this).position()['left']) + 'px');
				}										
				$(mapDiv).fadeIn(200, function() {$(this).dropShadow()});
				//$(mapDiv).dropShadow();				
				
			}
			else {
				$(mapDiv).removeShadow();
				$(mapDiv).fadeOut(200);
			}
		}
		else {
			// build the map
			var mapDiv = document.createElement( 'div' );
			$(mapDiv).addClass('geotag-map-container');
		
			// if there's enough space, we'll show it on top of the icon
			// and if not, below
			if((e.clientY + 300) > window.innerHeight) {
				//mapDiv.style.top = '-315px';
				$(mapDiv).css( "top", (Math.round($(this).position()['top']) - (300 + 10)) + 'px');
				$(mapDiv).css( "left", Math.round($(this).position()['left']) + 'px');
			}
			else {
				$(mapDiv).css( "top", (Math.round($(this).position()['top']) + 15) + 'px');
				$(mapDiv).css( "left", Math.round($(this).position()['left']) + 'px');
			}
			/*$(mapDiv).hide();*/
			$(this).append(mapDiv);
			
			// create and display the map
			var map = new GMap2(mapDiv);
			var coords = eval($(this).attr('data'));
			point = new GLatLng(coords[0], coords[1]);
			map.setCenter(point, 13);
	  		map.setUIToDefault();
			// add the marker
			var marker = new GMarker(point);
			map.addOverlay(marker);
		
			// and mark it as visible
			this['mapAlreadyBuilt'] = true;
			
			$(mapDiv).fadeIn(200, function() {$(this).dropShadow()});
		}
		
		return(false);
	});
	
	/*$('.edit_entry').click(function(e) {
		// fetch the entry data
		$.Read('/service/entry/{id}', { id: this['rel'] }, parklife.callbacks.editEntry )
	});*/
	
	$('.note').each(function(i, e) {
		$(e).editable('/service/entry/' + $(e).attr('data-entry-id'), {
	      indicator : "<img src='/images/spinner.gif'>",
		  ajaxoptions: {type: 'PUT', dataType: 'json'},
	      type   : 'autogrow',
		  method: 'PUT',
	      select : true,
	      submit : 'OK',
	      cancel : 'cancel',
	      cssclass : "editable",
		  tooltip   : "Click to edit...",
		  onblur    : "ignore",
		  name: "text",
		  autogrow : {
		  	lineHeight : 16,
		    minHeight  : 32
		  },
		  callback: function(self,data) {
			// our restful services always return json 
			$(this).html(self.entry.text);
		  }
		})
	});
	
	//$('.title').editable('http://localhost:8081');	
	
});

parklife.callbacks.editEntry = function(resp)
{
	// hide the current entry
	$('#item_' + resp.entry_id).hide();
	
	// and now make the needed fields editable
	$("#item_wrapper_" + resp.entry_id).html('<div class="inline-editor-container">\
	  <textarea class="mceEditor inline-editor">' + resp.entry.text + '</textarea>\
	  </div>');	
	
	tinyMCE.init({
			theme : "advanced",
			mode : "specific_textareas",
			editor_selector : "mceEditor",
			plugins : "emotions, inlinepopups",
			theme_advanced_buttons1 : "bold,italic,underline,separator,strikethrough,bullist,numlist,outdent, indent,undo,redo,link,unlink,image, charmap, code",
			theme_advanced_buttons2 : "",
			theme_advanced_buttons3 : "",
			theme_advanced_toolbar_location : "top",
			theme_advanced_toolbar_align : "left",
			extended_valid_elements : "div[id,class,style],iframe[src|width|height|frameborder],object[width|height|type|data],embed[src|type|width|height|wmode|flashvars], param[name|value], a[name|href|target|title|onclick],img[width|class|src|border=0|alt|title|hspace|vspace|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],span[class|align|style], p",
			cleanup: "true",
			convert_urls : false,
			debug : false
	});	
}