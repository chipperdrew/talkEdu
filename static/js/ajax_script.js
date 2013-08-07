$(document).ready(function() {

var create_vote = function() {
	var args = { type:"GET", url:$(this).attr('href'), data:{},
			success: function(data) { 
			if(data) {
				if(data["item_type"]=='c') {
					var canv = document.getElementById("commentCanvas"+data["post_id"]);
				} else {
					var canv = document.getElementById("myCanvas"+data["post_id"]);
				}
				var draw = canv.getContext("2d");
				clearPulse(draw); //Clear canvas and redraw
				drawEntireChart(draw, data["user_color_dict"], data["post_dict"], data["post_mid"], true);
	
				// Reload div that displays overall percentage and number of votes
				if(data["item_type"]=='c') {
					// For consistency (otherwise displays "1" and "0")
					if(data["post_mid"]==1 || data["post_mid"]==0) {
						data["post_mid"] = data["post_mid"] + '.0';
					}
					// Load doesn't work after "show replies", so HTML is hard-coded :(
					$('.comstats'+data["post_id"]).html("Overall: "+data["post_mid"]+ "<br>Total Votes: "+data["post_total"]);
				} else {
					$('.poststats'+data["post_id"]).load(' .poststats'+data["post_id"]);
				}
			}}};
	$.ajax(args);
	return false;
};


var mark_as_spam = function() {
	var args = { type:"GET", url:$(this).attr('href'), data:{},
			success: function(data) { 
			if(data) {
				// Add comment indicating spam marking received
				var textNode = document.createTextNode(" Thanks!");
				//TOFIX LATER: Should be able to access w/o need for id (like via $(this).parent)
				if(data["item_type"]=='p') {
					var child = document.getElementById('post_links'+data["id"]);
					child.parentNode.insertBefore(textNode, child.nextSibling);
				} else {
					var span = document.createElement('span');
					span.style.color = "#ff982c";
					span.appendChild(textNode);
					var child = document.getElementById('comment_links'+data["id"]);
					child.parentNode.insertBefore(span, child.nextSibling);
				}
			}}};
	$.ajax(args);
	return false;
};

var show_replies = function() {
	var args = { type:"GET", url:$(this).attr('href'), data:{},
			success: function(data) { 
			if(data) {
				// Reload comment_display.html
				$('#commenters').html(data);
			}}};
	$.ajax(args);
	return false;
};


$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});		
			
			var csrftoken = getCookie('csrftoken');
			$("body").on("click", ".up", create_vote);
			$("body").on("click", ".down", create_vote);
			$("body").on("click", ".spam", mark_as_spam);
			$("body").on("click", ".show_replies", show_replies);
});


// AJAX CSRF functions
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
