(function(window) {
	var app = function() {}

	app.currentPage = 1;

	app.prototype.init = function() {
		console.log("Mobile Parklife initialized");	
	}

	app.showStreamPost = function(urlObj, options) {
		//var link = urlObj.search.replace( /.*post=/, "" ) + "?f=json";	// TODO: it probably isn't a good idea to hardcode this
		//var page = "#stream-post";

		var page = "#stream-post";
		var link = urlObj.pathname.replace("/!", "") + "?f=json";

		console.log("link=" + link + "\npage=" + page);

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
				$(page).children(":jqmData(role=content)").find(".date-timestamp").html(entry.created.isoformat);
				options.dataUrl = urlObj.href;
				$(page).page();
				$.mobile.changePage($(page), options);
			}
		});	
	}

	app.renderStreamItem = function(entry) {		
		var content = "<li>";

		buildMobileLink = function(url) {
			return(/*"/!" + */$.mobile.path.parseUrl(url).pathname);
		}

		// icon markup
		var icon = '<img src="/images/' + entry.source + '.png" class="ui-li-icon" />';
		// date markup
		var date = '<p class="date-timestamp" data-timestamp="' + entry.created.isoformat + '">' + entry.created.isoformat + '</p>';
		
		if(entry.source == 'blog') {
			content += '<a href="' + buildMobileLink(entry.permalink) + '">' + icon +
					   date +	
					   '<h3>' + entry.title + '</h3>' +
					   '</a>';
		}
		else if(entry.source == 'instagram') {
			content += '<a href="' + entry.url + '">' + icon + date + entry.title + entry.text +
					   '</a>';			
		}
		else {
			content += '<a href="' + entry.url + '">' + icon + date + app.removeHTML(entry.text) + '</a>';					   
		}
				
		content += "</li>"

		return(content);
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
					content += app.renderStreamItem(entry);
				});				
				//$('#stream-list').html(content).listview('refresh');
				$('#stream-list').html($('#stream-list').html() + content).listview('refresh');
				$('.date-timestamp').cuteTime({ refresh: 60000 });
				$.mobile.hidePageLoadingMsg();
			}
		})		
	}

	app.displayMore = function() {
		app.currentPage++;
		app.displayPage(app.currentPage);

		console.log("Current page = " + app.currentPage);
	}

	var routes = {
		post: {
			match: /\/entry\//,
			handler: function(params) {
				app.showStreamPost(params.u, params.data.options);
			}
		}
	}

	// This is our mini controller - if no route matches the list, it will be given
	// to jQueryMobile for standard processing
	app.pageBeforeChangeHandler = function(e,data) {
		if(typeof data.toPage === "string") {

			console.log("Looking for route to match: " + data.toPage);

			var u = $.mobile.path.parseUrl( data.toPage );
			var routeFound = false;
			for(route in routes) {				
				if(u.pathname.search(routes[route].match) > -1) {
					// call the handler
					console.log("Found match with route: " + route);
					routes[route].handler({u: u, data:data, event:e});
					// prevent execution of the default event and exit the loop
					e.preventDefault();
					routeFound = true;
					break;
				}
			}

			// TODO: is this needed?
			/*if(!routeFound) {
				routes.default.handler({u: u, data:data, event:e});
				e.preventDefault();
			}*/

			return;
		}
	}

	app.removeHTML = function(s) {
		// remove all tags and multiple blank spaces
		return(s.replace(/<(?:.|\n)*?>/gm, ' ').trim().replace(/\s+/, ' '));
	}

	window.app = app;
})(window);

$(document).ready(function(){
	app = new app();
	app.init();		
});

// handler that loads the front page
$( '#main' ).live( 'pageinit', function() {
	app.displayPage(1);

	// "more..." button handler - TODO: if this is placed elsewhere, the event handler does not get triggered
	$("#more-button").bind( "click", app.displayMore);
});

// handles click events
$(document).bind( "pagebeforechange", app.pageBeforeChangeHandler);