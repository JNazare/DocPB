const photo_width = 900;
const photo_height = 675;

$(document).ready(function() {
	const video = $("#video").get(0);

	const constraints = {
		audio: true,
		video: {
			width: photo_width,
			height: photo_height
		}
	};

	// Access webcam
	async function init() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia(
				constraints
			);
			handleSuccess(stream);
		} catch (e) {
			console.log(e.toString());
		}
	}

	// Success
	function handleSuccess(stream) {
		window.stream = stream;
		video.srcObject = stream;
	}

	// Load init
	init();

	// Draw image

	var seconds = 9;
	$("#timer").text(seconds);
	var x = setInterval(function() {
		seconds = seconds - 1;
		if (seconds <= 0) {
			$("#timer").text("");
			clearInterval(x);
			takePhoto();
		} else {
			$("#timer").text(seconds);
		}
	}, 1000);
});

function takePhoto() {
	var counter = window.location.pathname.split("/").pop();
	const canvas = $("#canvas").get(0);
	var context = canvas.getContext("2d");
	context.drawImage(video, 0, 0, photo_width, photo_height);
	$("#video").hide();
	var b64image = canvas.toDataURL("image/png");
	$.post("/capture/" + counter, { b64image: b64image }).then(function(
		redirect_url
	) {
		window.location.href = redirect_url;
	});
}
