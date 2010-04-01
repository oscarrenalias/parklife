parklife.tinymce = Object();

// we need this so that TinyMCE doesn't mess up the content
// in <pre> blocks
parklife.tinymce.CustomCleanup = function(type, content) 
{
	switch (type) {
		case "get_from_editor":
			content = content.replace(/<br\s*\/>/gi, "\n");
			break;
		case "insert_to_editor":
		break;
	}

  return content;
}