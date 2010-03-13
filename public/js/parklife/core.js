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
	$.Delete('/admin/entry/{id}', { id: entry_id }, parklife.callbacks.deleteEntry )
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
	$.each(resp.responseData.results, function(i, result) {			
		code = '<div class="search-result" id="search-result-' + i + '">\
		<div class="search-result-title"><a href="' + result.url + '">' + result.title + '</a></div>\
		<div class="search-result-content">' + result.content +'</div>\
		</div>\n';
		resultData += code;
	});
	// and show the cursor
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
		data: { "v": "1.0", "q": terms, "cx": "011990932543207137146:wcze-5xmxso", "start": start, "rsz": "large", "key": parklife.config.GOOGLE_API_KEY },
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
}

parklife.events.searchKeyHandler = function(event)
{	
	if(event.keyCode == 13) {
		$('#submitSearchButton').click();
		event.preventDefault();
	}
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
	// set the event handler for editing entries
	$(".edit_entry").each(function(index) {
		$(this).click(function(e) {
			if(e.target.tagName.toLowerCase()=='img') id = e.target.parentNode.rel;
			else id = e.target.rel;
			parklife.editEntry(id); 
			return(false) 
		});
	});	
});