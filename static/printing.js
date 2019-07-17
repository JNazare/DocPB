$(document).ready(function() {
	seconds = 10;
	var x = setInterval(function() {
		seconds = seconds - 1;
		$("#timer").text(seconds);
	}, 1000);
	window.setTimeout(function() {
		window.location.href = "/";
	}, 10000);
});
