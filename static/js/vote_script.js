// Pulse bar and canvas dimensions
var canvasWidth = 150;
var canvasHeight = 100;
var leftArc = 15;
var bottomArc = 90;
var rad = 9;
var topOffset = 1;
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

// Clears the pulse grid and redraws outline
function clearPulse() {
	draw.clearRect(0, 0, canvasHeight, canvasWidth);
	drawPulseOutline();
}
	

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
}


// Draws the pulse bars depending on percentage of up votes
function drawPulse(perc, offset, draw) {
	if(perc == 0) {
		null
	} else if(perc <= arcPerc) {
		// Draw part of bottom arc
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percArea = perc*totalArea;
		var num = 2*percArea/Math.pow(rad,2);
		// Root finding using Newton's Method --- theta - sin(theta) - num = 0
		var tol = 0.01;
		var theta = num;
		var f = theta - Math.sin(theta) - num;
		var fPrime = 1 - Math.cos(theta);
		while(Math.abs(f) > tol) {
			thetaPrev = theta;
			theta = thetaPrev - (f/fPrime);
			f = theta - Math.sin(theta) - num;
			fPrime = 1 - Math.cos(theta);
		}
		// Using found theta to draw arc
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc, rad, (Math.PI-theta)/2, (Math.PI+theta)/2);
		draw.closePath();
		draw.fill();		
			
	} else if(perc <= 1 - arcPerc) {
		// Draw bottom arc and part of rect
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc, rad, 0*Math.PI, 1*Math.PI);
		draw.closePath();
		draw.fill();
		var rectHeightPerc = (perc - arcPerc)/rectPerc;
		draw.rect(leftArc-rad+offset, (height+rad)-(height*rectHeightPerc)+topOffset, 2*rad, rectHeightPerc*height);
		draw.fill();
	} else {
		// Draw bottom arc, rect, and part of top arc
		// Drawing bottom arc and rect
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc, rad, 0*Math.PI, 1*Math.PI);
		draw.closePath();
		draw.fill();
		var rectHeightPerc = (perc - arcPerc)/rectPerc;
		draw.rect(leftArc-rad+offset, rad+topOffset, 2*rad, height);
		draw.fill();

		// Drawing top arc by finding UNCOLORED area
		// Area of circular segment = R^2/2*(theta - sin(theta))
		var percAreaFromTop = (1-perc)*totalArea;
		var num = 2*percAreaFromTop/Math.pow(rad,2);
		// Root finding using Newton's Method --- theta - sin(theta) - num = 0
		var tol = 0.01;
		var theta = num;
		var f = theta - Math.sin(theta) - num;
		var fPrime = 1 - Math.cos(theta);
		while(Math.abs(f) > tol) {
			thetaPrev = theta;
			theta = thetaPrev - (f/fPrime);
			f = theta - Math.sin(theta) - num;
			fPrime = 1 - Math.cos(theta);
		}
		// Using found theta to draw 2 arcs
		draw.beginPath();
		draw.arc(leftArc+offset, bottomArc-height, rad, -(Math.PI-theta)/2, 0*Math.PI);
		draw.arc(leftArc+offset, bottomArc-height, rad, 1*Math.PI, -(Math.PI+theta)/2);
		draw.closePath();
		draw.fill();		
	}
}

