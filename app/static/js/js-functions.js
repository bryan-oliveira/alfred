/**
 * Created by boliveira on 09/22/16.
 */

function get_recipes_by_tag(url) {

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementsByClassName("recipe_list")[0].innerHTML = xhr.responseText;
        }
    }

    xhr.open('POST', url, true);

    xhr.onload = function (e) {
        console.log(e);
    }

    xhr.send();
}

function start_siriwave() {
    document.getElementById('siri-container').style.visibility = 'visible';
    SW.start();
}

function stop_siriwave() {
    SW.setSpeed(0.1);
    SW.setAmplitude(0.1);
    SW.stop();
    document.getElementById('siri-container').style.visibility = 'hidden';
}