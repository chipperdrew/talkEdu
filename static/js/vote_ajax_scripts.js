// Pulse bar and canvas dimensions
var canvasWidth = 125;
var canvasHeight = 100;
var leftArc = 15;
var bottomArc = 90;
var rad = 9;
var topOffset = 1; // Prevents top of chart from being cut off
var height = bottomArc-rad-topOffset;
var numberOfTypes = 5;
var separationDist = 25;

// Vars used in various calcuations
var arcArea = 0.5*Math.pow(rad,2)*Math.PI;
var rectArea = 2*rad*height;
var totalArea = 2*arcArea + rectArea;
var arcPerc = arcArea/totalArea;
var rectPerc = rectArea/totalArea;



// FUNCTIONS
function drawEntireChart(draw, colorDict, postVotesDict, middlePerc, isAjax) {
	// Convert Django strings to objects and iterate over objects to draw vote chart
	if(!isAjax) {
		colorDict = colorDict.replace(/&#39;/g, "'"); //I could have passed the data as |safe, but XSS attack?
		colorDict = colorDict.replace(/'/g, '\"');
		colorDict = JSON.parse( colorDict );
		postVotesDict = postVotesDict.replace(/&#39;/g, "'");
		postVotesDict = postVotesDict.replace(/'/g, '\"');
		postVotesDict = JSON.parse( postVotesDict );
	}
	i = 0;
	for(var user_type_key in colorDict) {
		draw.fillStyle = colorDict[user_type_key];
		drawPulse(draw, postVotesDict[user_type_key][2], separationDist*(i));
		i++;
	}
	drawMiddle(draw, middlePerc);
};


// Clears the pulse grid and redraws outline
function clearPulse(draw) {
	draw.clearRect(0, 0, canvasWidth, canvasHeight);
	drawPulseOutline(draw);
};
	

// Draws the outline of the pulse
function drawPulseOutline(draw) {
	draw.lineWidth = 1;
	for (var i=0; i<numberOfTypes*separationDist; i+=separationDist) {
		draw.beginPath();
		draw.arc(leftArc+i, bottomArc, rad, 0*Math.PI, 1*Math.PI);
		draw.arc(leftArc+i, bottomArc-height, rad, 1*Math.PI, 2*Math.PI);
		draw.closePath();
		draw.stroke();
	}
};

// Draws the pulse bars depending on percentage of up votes
function drawPulse(draw, perc, offset) {
	if(perc == 0) {
		null
	} else if(perc <= arcPerc) {
		// Draw part of bottom arc
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percArea = perc*totalArea;
		var theta = rootFindingHelper(percArea);
		// Using found theta to draw arc
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc, rad, (Math.PI-theta)/2, (Math.PI+theta)/2);
		draw.closePath();
		draw.fill();		
			
	} else if(perc <= 1 - arcPerc) {
		// Draw bottom arc and part of rect
		drawEntireBottomArcHelper(draw, offset);
		var rectHeightPerc = (perc - arcPerc)/rectPerc;
		draw.rect(leftArc-rad+offset, (height+rad)-(height*rectHeightPerc)+topOffset, 2*rad, rectHeightPerc*height);
		draw.fill();
	} else {
		// Draw bottom arc, rect, and part of top arc
		// Drawing bottom arc and rect
		drawEntireBottomArcHelper(draw, offset);
		draw.rect(leftArc-rad+offset, rad+topOffset, 2*rad, height);
		draw.fill();

		// Drawing top arc by finding UNCOLORED area
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percAreaFromTop = (1-perc)*totalArea;
		var theta = rootFindingHelper(percAreaFromTop);		
		// Using found theta to draw 2 arcs
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc-height, rad, -(Math.PI-theta)/2, 0*Math.PI);
		draw.arc(leftArc+offset, bottomArc-height, rad, 1*Math.PI, -(Math.PI+theta)/2);
		draw.closePath();
		draw.fill();		
	}
}

// Given the overall percentage, draws the middle line on the vote chart
function drawMiddle(draw, perc) {
	draw.lineWidth = 3;
	var lineStart = leftArc-rad;
	var lineEnd = 5*separationDist;	
	if(perc == 0 || perc == 1) {
		null
	}  else if(perc <= arcPerc) {
		// MIDDLE LINE IN BOTTOM SEMICIRCLE
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percArea = perc*totalArea;
		var theta = rootFindingHelper(percArea);		
		// Using found theta to determine height
		var heightOn = rad*Math.sin(theta);
		drawMiddleLineHelper(draw, lineStart, lineEnd, bottomArc+heightOn);	
	} else if(perc <= 1 - arcPerc) {
		// MIDDLE LINE IN RECTANGLE
		var rectHeightPerc = (perc - arcPerc)/rectPerc;
		var lineHeight = (height+rad)-(height*rectHeightPerc)+topOffset
		drawMiddleLineHelper(draw, lineStart, lineEnd, lineHeight);
	} else {
		// MIDDLE LINE IN TOP SEMICIRCLE
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percAreaFromTop = (1-perc)*totalArea;
		var theta = rootFindingHelper(percAreaFromTop);
		// Using theta to determine height				
		var bottomOfCircle = bottomArc-height;
		var heightOff = rad*Math.sin(theta);
		drawMiddleLineHelper(draw, lineStart, lineEnd, bottomOfCircle-heightOff);
	}
}


// HELPER FUNCTIONS
// Finds a theta approximation, used in drawPulse
function rootFindingHelper(percArea) {
	var num = 2*percArea/Math.pow(rad,2);
	// Finding theta using root finding (Newton's Method): theta - sin(theta) - num = 0.
	var tol = 0.1;
	var theta = num; // THETA=0 ==> 0% area
	var f = theta - Math.sin(theta) - num;
	var fPrime = 1 - Math.cos(theta);
	while(Math.abs(f) > tol) {
		thetaPrev = theta;
		theta = thetaPrev - (f/fPrime);
		f = theta - Math.sin(theta) - num;
		fPrime = 1 - Math.cos(theta);
	}
	return theta;
}

// Draws entire bottom arc, used in drawPulse
function drawEntireBottomArcHelper(draw, offset) {
	draw.beginPath();
	draw.arc(leftArc+offset, bottomArc, rad, 0*Math.PI, 1*Math.PI);
	draw.closePath();
	draw.fill();
}

// Draw the middle line, used in drawMiddle
function drawMiddleLineHelper(draw, x1, x2, height) {
	draw.beginPath();
	draw.moveTo(x1, height);
	draw.lineTo(x2, height);
	draw.stroke();
}


// ****************** AJAX SCRIPTS ***************
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


// Credit to 2 Scoops of Django
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


// AJAX CSRF functions -- Credit to Django docs CSRF page
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

// Credit to 2 Scoops of Django
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
