/**
 * Created by boliveira on 11/22/16.
 */

function get_recipes_by_tag() {
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

