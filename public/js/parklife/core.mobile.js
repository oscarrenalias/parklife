(function(window) {

	var app = function() {}
	var Router = function() {}

	/**
	 * The internal router handles click events between pages. Please note that this router
	 * only supports the pagebeforechange event
	 *
	 * Routes are defined in Router.routes. Make sure that the 'default' route is always
	 * the last one!
	 */
	Router.routes = {
		post: {
			match: /\/entry\//,
			handler: function(params) {
				app.showStreamPost(params.u, params.data.options);
			}
		},
		default: {	// the default handler simply shows the current page, whatever it is
			match: ".*",
			handler: function(params) {
				console.log("Executing default route - page: " + app.currentPage);
				app.displayPage(app.currentPage);
			}
		}
	}

	// this hooks up our route handler to jQueryMobile's pageBeforeChangeHandler
	Router.pageBeforeChangeHandler = function(e, data) {
		if(typeof data.toPage === "string") {
			Router.handler(e, data);
			return;
		}	
	}	

	/**
	 * Core function of our little handler, which maps internal URLs to routes within
	 * the application.
	 */
	Router.handler = function(e,data) {
		console.log("Looking for route to match: " + data.toPage);

		var u = $.mobile.path.parseUrl( data.toPage );
		var routeFound = false;
		for(route in Router.routes) {				
			if(u.pathname.search(Router.routes[route].match) > -1) {
				// call the handler
				console.log("Found match with route: " + route);
				Router.routes[route].handler({u: u, data:data, event:e});
				// prevent execution of the default event and exit the loop
				e.preventDefault();
				routeFound = true;
				break;
			}
		}
	}

	app.currentPage = 1;

	/**
	 * Initializes the application ('app')
	 */
	app.prototype.init = function() {
		console.log("Mobile Parklife initialized");
		$(document).bind( "pagebeforechange", Router.pageBeforeChangeHandler);

		$("#more-button").bind( "click", function() {
			// increase the current page
			app.currentPage++;
			// and then jump into our router to take care of calling the right handler
			Router.handler(document.createEvent("Event"), {toPage: window.location.href, options:{}});
		});

		// increase the refresh date for the timestamps
		$.timeago.settings.refreshMillis = 6000;
	}

	/**
	 * Retrieves a post from the REST endpoint. This is only used to show blog posts, since
	 * anything else points to the permalink from the source (twitter, instagram, etc)
	 *
	 * TODO: move this into a proper model-based structure
	 */
	app.showStreamPost = function(urlObj, options) {
		var page = "#stream-post";
		var link = urlObj.pathname.replace("/!", "") + "?f=json";

		$.ajax({
			url: link,
			dataType: "json",
			error: function() {
				window.alert("There was an error loading the content");
			},
			success: function(results) {
				var entry = results.entry;
				$(page).children(":jqmData(role=content)").find("h2").html(entry.title);
				$(page).children(":jqmData(role=content)").find("#content").html(entry.text);
				$(page).children(":jqmData(role=content)").find("#tags").html("#" + entry.tags.join(" #"));
				$(page).children(":jqmData(role=content)").find("#timestamp").html(app.renderHTML5Date(entry.created.isoformat));
				options.dataUrl = urlObj.href;
				$(page).page();
				$.mobile.changePage($(page), options);
			}
		});	
	}

	app.renderHTML5Date = function(isoDate) {
		return('<time class="date-timestamp" datetime="' + isoDate + '">' + $.timeago(isoDate) + '</time>');
	}

	/**
	 * Renders an item from the mobile stream.
	 *
	 * All the rendering is done by stream-specific functions. For those that don't require 
	 * specific rendering logic, they point to the 'default' function
	 */
	app.renderItem = function(entry) {

		// generates links
		var buildMobileLink = function(url) {
			return(/*"/!" + */$.mobile.path.parseUrl(url).pathname);
		}
		// default icon markup
		var icon = '<img src="/images/' + entry.source + '.png" class="ui-li-icon" />';
		// default date markup
		var date = '<p>' + app.renderHTML5Date(entry.created.isoformat) + '</p>';

		// The functions in here render specific entry types, or simply default to the standard renderer if
		// they don't have any specific rendering needs
		var renderers = {
			// specific entry markup generators
			default: function(entry) {
				return(
					'<a href="' + entry.url + '">' + icon + date + app.removeHTML(entry.text) + '</a>'
				)
			},
			blog: function(entry) {
				return(
					'<a href="' + buildMobileLink(entry.permalink) + '">' + icon +
					   date +	
					   '<h3>' + entry.title + '</h3>' +
					   '</a>'
				)
			},
			instagram: function(entry) {
				return(
					'<a href="' + entry.url + '">' + icon + date + entry.title + entry.text + '</a>'
				)
			},
			// all these use the default 
			twitter: function(entry) { return(renderers.default(entry)) },
			youtube: function(entry) { return(renderers.default(entry)) },
			picasa: function(entry) { return(renderers.default(entry)) },
			pinboard: function(entry) { return(renderers.default(entry)) },
			delicious: function(entry) { return(renderers.default(entry)) },
		};

		return("<li>" + renderers[entry.source](entry) + "</li>");
	}

	app.displayPage = function(page) {

		$.mobile.showPageLoadingMsg();
		
		var url = "/?f=json";
		if(page > 1)
			url += "&p=" + page;

		$.ajax({
			url: url,
			dataType: "json",
			error: function() {
				$.mobile.hidePageLoadingMsg();
				window.alert("There was an error loading the data");				
			},
			success: function(data) {
				var content = "";
				$.each(data.entries, function(key, entry) {
					content += app.renderItem(entry);
				});
				//$('#stream-list').html(content).listview('refresh');
				$('#stream-list').html($('#stream-list').html() + content).listview('refresh');
				$("time.date-timestamp").timeago();	// this will automatically update timestamps
				$.mobile.changePage($("#main"));
				$.mobile.hidePageLoadingMsg();
			}
		})		
	}

	/**
	 * Utility method to remove all HTML tags
	 */
	app.removeHTML = function(s) {	
		return(s.replace(/<(?:.|\n)*?>/gm, ' ').trim().replace(/\s+/, ' '));
	}

	app.run = function() {		
		// redirect all requests straight away to our route handler
		Router.handler(
			document.createEvent("Event") /* TODO: is this enough? */, 
			{ toPage: window.location.href, options: {}}	/* TODO: this a bit hackish... */
		);
	}

	window.app = app;

})(window);

$(document).ready(function() {
	app = new app();
	app.init();		
});

// handler that loads the front page
$( '#main' ).live( 'pageinit', app.run);