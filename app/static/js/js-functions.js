/**
 * Created by boliveira on 09/22/16.
 */

var timeoutID = 0;
var siri_is_on = false;

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
    siri_is_on = true;
    window.clearTimeout(timeoutID);
    $('#text_div').fadeOut();
    $('.alfred_input').fadeOut();
    $('#siri-container').css('visibility', 'visible');
    $('#siri-container').fadeIn();
    SW.start();
}

function stop_siriwave() {
    SW.setSpeed(0.1);
    SW.setAmplitude(0.1);
    SW.stop();
    $('#siri-container').css('visibility', 'hidden');
    $('.alfred_input').fadeIn();
}

function show_alfred_tooltip() {
    timeoutID = window.setTimeout(run_tooltip_code, 1000);
}

function run_tooltip_code() {
    $('.alfred_input').fadeOut();

    $('#siri-container').fadeOut();
    //$('#siri-container').css('visibility', 'hidden');
    //$('#text_div').css('visibility', 'visible');
    $('#text_div').fadeIn();

    var t1 = $('<p class="small_text"></p>').text("Click Alfred. Ask for recipes based on ingredients or meal types.");
    var t2 = $('<p class="small_text"></p>').text("Click Alfred again when finished speaking.");

    $('#text_div').append(t1, t2);
}

function hide_alfred_tooltip() {
    window.clearTimeout(timeoutID);

    /* If siri waves are on, ignore normal behavior */
    if (siri_is_on == true)
        return true;

    /* Else, hide tooltip and bring fade input field back in */
    $('#text_div').fadeOut();
    $('#text_div').text('');

    $('.alfred_input').css('visibility', 'visible');
    $('.alfred_input').fadeIn();
}

/* Timer function to start/stop timer */
function initializeClock(id, duration, alarmeSound) {
    /* Set end time */
    var end_time = new Date().getTime();
    end_time = end_time + (duration * 60000);

    var timer = setInterval(function () {
        var clock = document.getElementById(id);
        var now = new Date().getTime();

        /* Calculate remaining time */
        var dist = parseInt(end_time - now, 10);
        //console.log(dist);

        /* Calculate time remaining */
        var hours = parseInt(Math.floor(dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var min = parseInt(Math.floor(dist % (1000 * 60 * 60 * 60)) / (1000 * 60));
        var secs = parseInt(Math.floor(dist % (1000 * 60)) / 1000);

        /* Pad time with zeros */
        if (hours < 10) {
            hours = '0' + hours;
        }
        if (min < 10) {
            min = '0' + min;
        }
        if (secs < 10) {
            secs = '0' + secs;
        }

        clock.innerHTML = hours + ':' + min + ':' + secs;

        if (hours == 0 && min == 0 && secs == 0) {
            clearInterval(timer);
            soundAlarme(alarmeSound);
        }
    }, 1000);
}

/* Sound alarm */
function soundAlarme(audio) {
    audio.play();
}