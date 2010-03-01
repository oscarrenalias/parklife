/**
 * Parklife core javascript functions
 */

parklife = Object();

parklife.updateEntry = function(entry_id)
{
	return(false);	
}

parklife.editEntry = function(entry_id)
{
	return(false);	
}

parklife.callbacks = Object();

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