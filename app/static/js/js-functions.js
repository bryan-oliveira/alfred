/**
 * Created by boliveira on 11/22/16.
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

function confirm_del_account() {
    
}