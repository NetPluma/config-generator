console.log("templateFiller.js")

const SUCCESS_COLOR = 'rgb(163, 242, 17)';
const ERROR_COLOR = 'rgb(252, 83, 83)';


//let fill_template_button = document.getElementById("fill-template")

// deprecated with ACE editor
//let yaml_input = document.getElementById("yaml-input");
//let jinja_template_input = document.getElementById("jinja-template-input");
if (window.location.pathname === 'http://127.0.0.1:8000/templateFiller/') {
    // Execute specific JavaScript code for this URL
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('fill-template').addEventListener('click', create_config_from_template);
    });
}

if (window.location.href.includes('Excel-Config/')) {
    // Execute specific JavaScript code for this URL
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('fill-multiple-template').addEventListener('click', create_multiple_configs_from_template);
    });
}



// create a single config 
function create_config_from_template()
{
    // deprecated with ACE editor
    //let yaml_content = yaml_input.value
    //let jinja_content = jinja_template_input.value

    let yaml_content = yaml_editor.getSession().getValue();
    let jinja_content = template_editor.getSession().getValue();

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/generate-config/', true); 
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Include CSRF token

    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Handle success
            console.log('Response:', this.responseText);
            var response = JSON.parse(this.responseText);
            console.log(response);
            output_editor.getSession().setValue(response["data"]);
        }
    }
    xhr.send(JSON.stringify({yaml_content: yaml_content, jinja_content: jinja_content}));
    console.log("creating template")  
}

// create a single config 
function create_multiple_configs_from_template()
{
    // deprecated with ACE editor
    //let yaml_content = yaml_input.value
    //let jinja_content = jinja_template_input.value

    let yaml_content = yaml_editor.getSession().getValue();
    let jinja_content = template_editor.getSession().getValue();

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/templateFiller/ajax/generate-multiple-configs/', true); 
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Include CSRF token

    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Handle success
            console.log('Response:', this.responseText);
            var response = JSON.parse(this.responseText);
            console.log(response);
            output_editor.getSession().setValue(response["data"]);
        }
    }
    xhr.send(JSON.stringify({yaml_content: yaml_content, jinja_content: jinja_content}));
    console.log("creating template")  
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// JQuery

jQuery.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", jQuery('[name="csrfmiddlewaretoken"]').val());
        }
    }
});

jQuery(document).ready(function(){
    jQuery('#spreadsheet-input').submit(function(event){
        event.preventDefault();  // Prevent default form submission

        message_box = document.getElementById('spreadsheet-message-box');

        jQuery.ajax({
            type: 'POST',
            url: '/templateFiller/ajax/upload-excel/',  // URL to send the form data to
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function(response){
                // Handle success: update part of your page, show a message, etc.
                document.getElementById('spreadsheet-submit-button').style.backgroundColor = SUCCESS_COLOR;
                message_box.innerHTML = response.message ;
                message_box.style.color = SUCCESS_COLOR;
                message_box.style.opacity = 1;
                document.getElementById('fill-multiple-template').disabled = false;
            },
            error: function(xhr, errmsg, err){
                // Handle error
                document.getElementById('spreadsheet-submit-button').style.backgroundColor = ERROR_COLOR;
                message_box.innerHTML = errmsg;    
                message_box.style.color = ERROR_COLOR;
                message_box.style.opacity = 1;
            }
        });
    });
});