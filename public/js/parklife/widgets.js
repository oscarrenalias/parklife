/**
 * Basic widget-like functionality that pull data from the jsonp feeds
 * and allow to incorporate them into any existing page
 */

parklife.widgets = Object();
parklife.widgets.baseUrl = "http://stream.renalias.net";
parklife.widgets.blogUrl = parklife.widgets.baseUrl + "/source/blog";
parklife.widgets.twitterUrl = parklife.widgets.baseUrl + "/source/twitter";
parklife.widgets.rssUrl = parklife.widgets.baseUrl + "/source/googlereader";
parklife.widgets.deliciousUrl = parklife.widgets.baseUrl + "/source/delicious";
parklife.widgets.youtubeUrl = parklife.widgets.baseUrl + "/source/youtube";

parklife.widgets.latestPost = function() {
	parklife.widgets.generic({url:parklife.widgets.blogUrl + "?f=json", success:function(data) {
		entry = data.entries[0];
		$('#latest-blog-post-content').html('<a href="' + entry.permalink + '">' + entry.title + '</a>, posted ' + $.timeago(entry.created.ctime));
		$('#latest-blog-post').fadeIn();		
	}})
}

parklife.widgets.latestTweet = function() {
	parklife.widgets.generic({url:parklife.widgets.twitterUrl + "?f=json", success:function(data) {
		entry = data.entries[0];
		$('#latest-tweet-content').html(entry.text + ", posted " + $.timeago(entry.created.ctime));
		$('#latest-tweet').fadeIn();		
	}});
}

parklife.widgets.latestArticle = function() {
	parklife.widgets.generic({url:parklife.widgets.rssUrl + "?f=json", success:function(data) {
		entry = data.entries[0];
		$('#latest-rss-content').html('<a href="' + entry.url + '">' + entry.title + '</a>, posted ' + $.timeago(entry.created.ctime));
		$('#latest-rss').fadeIn();		
	}})
}

parklife.widgets.latestLink = function() {
	parklife.widgets.generic({url:parklife.widgets.deliciousUrl + "?f=json", success:function(data) {
		entry = data.entries[0];
		$('#latest-delicious-content').html('<a href="' + entry.permalink + '">' + entry.title + '</a>, added ' + $.timeago(entry.created.ctime));
		$('#latest-delicious').fadeIn();		
	}})
}

parklife.widgets.latestVideo = function() {
	parklife.widgets.generic({url:parklife.widgets.youtubeUrl + "?f=json", success:function(data) {
		entry = data.entries[0];
		$('#latest-youtube-content').html('<a href="' + entry.permalink + '">' + entry.text + '</a>, added ' + $.timeago(entry.created.ctime));
		$('#latest-youtube').fadeIn();		
	}})
}

parklife.widgets.generic = function(params) {
	$.ajax({url:params.url, dataType:"jsonp", success: function(data) {
		if( data.entries[0]) {
			params.success(data);
		}
	}});
}