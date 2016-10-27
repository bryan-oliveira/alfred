// fork getUserMedia for multiple browser versions, for the future
// when more browsers support MediaRecorder

navigator.getUserMedia = (  navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia ||
                            navigator.msGetUserMedia );

// set up basic variables for app
var record = document.querySelector('.microphone');

//main block for doing the audio recording
if (navigator.getUserMedia) {

    console.log('getUserMedia is supported.');

    var constraints = {audio: true, mimeType: "audio/webm; codec=vorbis"};
    var chunks = [];


    var onSuccess = function (stream) {
        var mediaRecorder = new MediaRecorder(stream, constraints);

        record.onclick = function () {
            // Is recording; We want to stop
            if (record.classList.contains("active")) {
                mediaRecorder.stop();
                record.style.background = "None";
                record.classList.remove("active");
                console.log(mediaRecorder.state);
                console.log("recorder stopped");
            }
            // Start recording
            else {
                mediaRecorder.start();
                record.style.background = "gray";
                record.classList.add("active");
                console.log(mediaRecorder.state);
                console.log("recorder started");
            }
        }

        mediaRecorder.onstop = function (e) {

            var blob = new Blob(chunks, {'type': 'audio/ogg;'});
            console.log('Chunks size:' + chunks.length);
            console.log("Blob:" + blob);
            chunks = [];

            //var audioURL = window.URL.createObjectURL(blob);
            //audio.src = audioURL;

            console.log("recorder stopped");

            // Send blob to server
            var formData = new FormData();
            formData.append('audio', blob);

            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function (response) {
                if (xhr.readyState == 4) {
                    document.getElementsByClassName("recipe_list")[0].innerHTML = xhr.responseText;
                }
            }

            xhr.open('POST', '/upload', true);

            xhr.onload = function (e) {
                console.log('NEW MESSAGE');
                console.log(e);
            }

            xhr.send(formData);

        }

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        }
    }

    var onError = function (err) {
        console.log('The following error occured: ' + err);
    }

    navigator.getUserMedia(constraints, onSuccess, onError);

} else {
    console.log('getUserMedia not supported on your browser!');
}

