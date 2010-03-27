parklife.forms = Object();
parklife.forms.callbacks = Object();

parklife.forms._getBlogFormData = function()
{
	// depending on whether tinymce is running or not
	// text needs to be extracted differently
	if(typeof(tinyMCE) != "undefined")
		text = tinyMCE.get('id_text').getContent();
	else
		text = $('#id_text').val();
	
	return({
		'title': $('#id_title').val(),
		'text': text,
		'tags': $('#id_tags').val(),
		'lat': $('#id_lat').val(),
		'lng': $('#id_lng').val()
	});
}

parklife.forms.callbacks.submitBlogForm = function(resp)
{
	// before anything, hide any previous errors
	$('.field_errors').hide('fast');		
	$('.field_errors').remove();	
	// hide the spinner
	$('#spinner').remove();
	
	if( resp.error ) {		
		// there were errors, show them in the correct place
		for( fieldName in resp.errors ) {
			fieldErrors = '<ul class="field_errors">';
			for( j in resp.errors[fieldName] ) {
				// a field can actually have multiple errors
				fieldErrors += '<li>' + resp.errors[fieldName][j] + '</li>\n';
			}
			fieldErrors += '</ul>';
			$('#id_' + fieldName).after(fieldErrors);
		}
	}
	else {		
		// show an acknowledgement message
		$('#form_messages').html('<div class="success_message" style="display:none">' + resp.message + '</div>');
		// the message will hide itself after 5 seconds, should be enough
		$('.success_message').show('slow').delay(5000).hide('slow');		
	}
}

parklife.forms.blogClickHandler = function()
{
	// if the 'id_entry' field containing the entry key exists in the form, then we're doing
	// an update of an existing field. Otherwise we're doing an insertion
	entry_id = $('#id_entry').val();
	if( !entry_id ) 
		$.post("/service/entry/", 
		       parklife.forms._getBlogFormData(),
		       function(resp) {
		          parklife.forms.callbacks.submitBlogForm(resp);
		          if( !resp.error) 
		          	$('#id_new_blog_entry')[0].reset();
		       }, 
		       "json" );	
	else 
		$.post("/service/entry/" + entry_id, parklife.forms._getBlogFormData(), parklife.forms.callbacks.submitBlogForm, "json" );	
		
	// show the spinner
	$('#submit_blog_entry').after('<img src="/images/spinner.gif" id="spinner" />');
	return( false );
}

$(document).ready(function() {
	$('#submit_blog_entry').click(parklife.forms.blogClickHandler);
});