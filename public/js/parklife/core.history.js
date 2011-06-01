(function(window,undefined){

	// Prepare our Variables
	var History = window.History;
	var $ = window.jQuery;
	var document = window.document;

	// Check to see if History.js is enabled for our Browser
	if ( !History.enabled ) {
		return false;
	}

	// Wait for Document
	$(function(){
		// Prepare Variables
		var contentSelector = '#content,article:first,.article:first,.post:first';
		var $content = $(contentSelector).filter(':first');
		var contentNode = $content.get(0);

		var $body = $(document.body);
		var rootUrl = History.getRootUrl();
		var scrollOptions = {
				duration: 800,
				easing:'swing'
			};

		// Ensure Content
		if ( $content.length === 0 ) {
			$content = $body;
		}

		// HTML Helper
		var documentHtml = function(html) {
			// Prepare
			var result = String(html)
				.replace(/<\!DOCTYPE[^>]*>/i, '')
				.replace(/<(html|head|body|title|meta|script)/gi,'<div class="document-$1"')
				.replace(/<\/(html|head|body|title|meta|script)/gi,'</div');

			// Return
			return result;
		};

		// Ajaxify Helper
		$.fn.ajaxify = function(){
			var $this = $(this);
			$this.find('a[rel="ajax"]').click(function(event) {
				var $this = $(this);
				var url = $this.attr('href');
				var title = $this.attr('title')||null;

				// Continue as normal for cmd clicks etc
				if ( event.which == 2 || event.metaKey ) { return true; }

				// Ajaxify this link
				History.pushState(null,title,url);
				event.preventDefault();
				return false;
			});

			return $this;
		};

		// Ajaxify all links marked with rel="ajax"
		$body.ajaxify();

		// Hook into State Changes
		$(window).bind('statechange',function(){
			// Prepare Variables
			var State = History.getState()
			var url = State.url;
			var relativeUrl = url.replace(rootUrl,'');

			// Set Loading
			$body.addClass('loading');

			// Start Fade Out
			// Animating to opacity to 0 still keeps the element's height intact
			// Which prevents that annoying pop bang issue when loading in new content
			$content.animate({opacity:0},500);

			// Ajax Request the Traditional Page
			$.ajax({
				url: url,
				data: "b=1",	// request Parklife to provide the content portion of the page only
				success: function(data, textStatus, jqXHR){
					var $data = $(documentHtml(data));
					var $dataContent = $data.filter(':first');					
					var contentHtml; 
					var $scripts;

					// Fetch the scripts
					$scripts = $dataContent.find('.document-script').detach();

					// Fetch the content
					contentHtml = $dataContent.html()||$data.html();
					if ( !contentHtml ) {
						document.location.href = url;
						return false;
					}

					// Update the content
					$content.stop(true,true);
					$content.html(contentHtml).animate({opacity:100}, 500).ajaxify(); //.show();

					// Add the scripts
					$scripts.each(function(){
						var scriptText = $(this).html(); 
						var scriptNode = document.createElement('script');
						scriptNode.appendChild(document.createTextNode(scriptText));
						contentNode.appendChild(scriptNode);
					});

					$('html, body').animate({ scrollTop: 0 }, 500);					
															
					$body.removeClass('loading');

					// Inform Google Analytics of the change
					if ( typeof window.pageTracker !== 'undefined' ) {
						window.pageTracker._trackPageview(relativeUrl);
					}
				},
				error: function(jqXHR, textStatus, errorThrown){
					document.location.href = url;
					return false;
				}
			});
		});
	});
})(window); 