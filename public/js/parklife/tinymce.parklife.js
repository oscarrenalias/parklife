parklife.tinymce = Object();

// we need this so that TinyMCE doesn't mess up the content
// in <pre> blocks
parklife.tinymce.CustomCleanup = function(type, content) 
{
	switch (type) {
		// gets passed when user submits the form
		case "get_from_editor":
			content = content.replace(/<br \/>/gi, "\n"); // would be nice if this replace only replaces the brs in a pre block. bur for the moment it is ok.
			break;
		// gets passed when new content is inserted into the editor
		case "insert_to_editor":
		break;
	}

  return content;
}