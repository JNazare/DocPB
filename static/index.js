$(document).ready(function() {
	$("#startbtn").click(function() {
		$.post("/").then(function(redirect_url) {
			window.location.href = redirect_url;
		});
	});
});
