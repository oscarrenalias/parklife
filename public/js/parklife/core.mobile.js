(function(window) {
	var app = function() {}

	app.prototype.init = function() {
		console.log("Mobile Parklife initialized");	
	}

	app.showStreamPost = function(urlObj, options) {
		var link = urlObj.search.replace( /.*post=/, "" ) + "?f=json";	// TODO: it probably isn't a good idea to hardcode this
		var page = "#stream-post";

		console.log("link=" + link + "\npage=" + page);

		$.ajax({
			url: link,
			dataType: "json",
			error: function() {
				window.alert("There was an error loading the content");
			},
			success: function(results) {
				var entry = results.entry;
				$(page).children(":jqmData(role=header)").find("h1").html(entry.title);
				$(page).children(":jqmData(role=content)").html(entry.text);
				options.dataUrl = urlObj.href;
				$(page).page();
				$.mobile.changePage($(page), options);
			}
		});	
	}

	app.initPage = function() {
		$.ajax({
			url:"/?f=json",
			dataType:"json",
			error: function() {
				window.alert("There was an error loading the data")
			},
			success: function(data) {
				var content = ""
				//for(entry in data.entries) { -- why doesn't this work?
				for(i=0; i<data.entries.length; i++) {
					entry = data.entries[i];
					text = entry.text;
					url = entry.permalink;
					if(entry.source=='blog') {
						text = entry.title; 
						//url = entry.permalink;
					}
					//content += '<li><a href="' + url + '">' + text + '</a></li>';
					content += '<li><a href="#stream-post?post=' + url + '">' + text + '</a></li>';
				}
				$('#stream-list').html(content).listview('refresh');
				//$('#stream-list').listview('refresh');
			}
		})		
	}

	app.pageBeforeChangeHandler = function(e,data) {
		if(typeof data.toPage === "string") {
			var u = $.mobile.path.parseUrl( data.toPage ),
			re = /^\?post=/;
			if ( u.search.search(re) !== -1 ) {
				app.showStreamPost(u, data.options)

				e.preventDefault();
			}
			return;
		}
	}

	window.app = app;
})(window);

$(document).ready(function(){
  app = new app();
  app.init();
});

// handler that loads the front page
$( '#main' ).live( 'pageinit', app.initPage);

// handles click events
$(document).bind( "pagebeforechange", app.pageBeforeChangeHandler);
