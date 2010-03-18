parklife.forms = Object();
parklife.forms.callbacks = Object();

parklife.forms._getBlogFormData = function()
{
	return({
		'title': $('#id_title').val(),
		'text': $('#id_text').val(),
		'tags': $('#id_tags').val()
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
		// no errors clean the form data
		$('#id_new_blog_entry')[0].reset();
		// show an acknowledgement message
		$('#form_messages').html('<div class="success_message" style="display:none">Blog entry added successfully</div>');
		// the message will hide itself after 5 seconds, should be enough
		$('.success_message').show('slow').delay(5000).hide('slow');		
	}
}

parklife.forms.blogClickHandler = function()
{
	$.post("/service/entry/", parklife.forms._getBlogFormData(), parklife.forms.callbacks.submitBlogForm, "json" );	
	// show the spinner
	$('#submit_blog_entry').after('<img src="/images/spinner.gif" id="spinner" />');
	return( false );
}

$(document).ready(function() {
	$('#submit_blog_entry').click(parklife.forms.blogClickHandler);
});