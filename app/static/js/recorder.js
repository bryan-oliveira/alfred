// fork getUserMedia for multiple browser versions, for the future
// when more browsers support MediaRecorder

navigator.getUserMedia = (  navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia ||
                            navigator.msGetUserMedia );

// set up basic variables for app
var record = document.querySelector('.alfred_image');

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
                stop_siriwave();
                $('#thinking-alfred').addClass('is-active');
            }
            // Start recording
            else {
                mediaRecorder.start();
                start_siriwave();
                record.style.background = "white";
                record.classList.add("active");
                console.log(mediaRecorder.state);
                console.log("recorder started");
            }
        };

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

                    $('#thinking-alfred').removeClass('is-active');
                    //document.getElementsByClassName("recipe_list")[0].innerHTML = xhr.responseText;
                    // Stop previous timers if any
                    clearInterval(window.alfred_timer);
                    document.body.innerHTML = "";
                    //window.location = 'about:blank';
                    document.write(xhr.responseText);

                    console.log($('#hidden-info').text());
                    // Get information from hidden field about ingredients (if any)
                    $('.alfred_input_text').val($('#hidden-info').text());
                }

            };

            xhr.open('POST', '/upload', true);

            xhr.onload = function (e) {
                console.log(e);
            };

            xhr.send(formData);

        };

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        }
    };

    var onError = function (err) {
        console.log('The following error occured: ' + err);
    };

    navigator.getUserMedia(constraints, onSuccess, onError);

} else {
    console.log('getUserMedia not supported on your browser!');
}

