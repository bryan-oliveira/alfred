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
    timeoutID = window.setTimeout(run_tooltip_code, 2000);
}

function run_tooltip_code() {
    $('.alfred_input').fadeOut();

    $('#siri-container').fadeOut();
    //$('#siri-container').css('visibility', 'hidden');
    //$('#text_div').css('visibility', 'visible');
    $('#text_div').fadeIn();

    var t1 = $('<p class="small_text"></p>').text("Click Alfred. Ask for recipes based on ingredients or meal types.");
    var t2 = $('<p class="small_text"></p>').text("Click Alfred again when finished speaking.");

    $('#text_div').append(t1,t2);
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

