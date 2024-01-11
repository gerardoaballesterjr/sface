var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.createElement('video');
var websocket = new WebSocket(canvas.getAttribute('data-websocket'));
var srcObject, interval;

function drawFrame() {
    var canvas_ = document.createElement('canvas');
    var context_ = canvas_.getContext('2d');
    canvas_.width = video.videoWidth;
    canvas_.height = video.videoHeight;
    context_.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas_.toBlob((blob) => {websocket.send(blob)}, 'image/jpeg', 0.8);
}

video.onplay = (event) => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    interval = setInterval(drawFrame, 100);
}

websocket.onmessage = (event) => {
    if (event.data instanceof Blob) {
        var image = new Image();
        image.onload = () => {context.drawImage(image, 0, 0, canvas.width, canvas.height)};
        image.src = URL.createObjectURL(event.data);
    }
}

function stop() {
    if (srcObject) {
        srcObject.getTracks().forEach(track => {
            track.stop();
        });
    }
    clearInterval(interval);
    srcObject = null;
    interval = null;
}

$('.modal').on('hide.bs.modal', function() {
    websocket.close();
    stop();
    setTimeout(function() {htmx.ajax('GET', location.href, '#base');}, 400);
});

websocket.onopen = (event) => {
    navigator.mediaDevices.getUserMedia({video:{facingMode:'environment',advanced:[{width:{exact:900}},]}}).then((stream) => {
        srcObject = stream;
        video.srcObject = stream;
        video.autoplay = true;
    }).catch((error) => {
        console.error(error);
    });
}