console.log("templateFiller.js")

const SUCCESS_COLOR = 'rgb(163, 242, 17)';
const ERROR_COLOR = 'rgb(252, 83, 83)';
const JINJA_HELPER_FIELD = document.getElementById('jinja-helper');    
let JINJA_VARIABLE_INTERVAL;
let JINJA_VARIABLE_INTERVAL_RUNNING = false;

template_editor.session.on('change', start_interval_timer );

//let fill_template_button = document.getElementById("fill-template")

// deprecated with ACE editor
//let yaml_input = document.getElementById("yaml-input");
//let jinja_template_input = document.getElementById("jinja-template-input");
//if (window.location.pathname === 'http://127.0.0.1:8000/templateFiller/') {
    
//}

if (window.location.href.includes('Excel-Config/')) {
    // Execute specific JavaScript code for this URL
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('fill-multiple-template').addEventListener('click', create_multiple_configs_from_template);
    });
}
else{
    // Execute specific JavaScript code for this URL
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('fill-template').addEventListener('click', create_config_from_template);
    });
}


//================================== Create a single Config =================================================================
// create a single config 
// This function is designed to send the contents of two editors (yaml_editor and template_editor)
// to a server endpoint via an AJAX POST request. It then handles the server's response by 
// updating an output_editor with the returned data
// Multiple Config will be generated as a result - the amout of configs generated depend on the 
// amout of devices defined in the Speadsheet file uploaded before
function create_config_from_template()
{
    let yaml_content = yaml_editor.getSession().getValue();
    let jinja_content = template_editor.getSession().getValue();

    // Create a new XMLHttpRequest object for making an AJAX request
    var xhr = new XMLHttpRequest();
    // Configure the request to be: POST, JSON and add CRSF Token
    xhr.open('POST', 'ajax/generate-config/', true); 
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Include CSRF token

    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Handle the successful response here
            // [...]
            console.log('Response:', this.responseText);
            var response = JSON.parse(this.responseText);
            console.log(response);
            // Set the response data to the output_editor
            output_editor.getSession().setValue(response["data"]);
        }
    }
    xhr.send(JSON.stringify({yaml_content: yaml_content, jinja_content: jinja_content}));
    console.log("creating template")  
}


//================================= Create Multiple Configs ==================================================================
// create a single config 
// This function is designed to send the contents of two editors (yaml_editor and template_editor)
// to a server endpoint via an AJAX POST request. It then handles the server's response by 
// updating an output_editor with the returned data
// Multiple Config will be generated as a result - the amout of configs generated depend on the 
// amout of devices defined in the Speadsheet file uploaded before
// 
// PRECONDITION: this function must only be called if a Spreadsheet has been uploaded before

function create_multiple_configs_from_template()
{
    // Retrieve the content from the yaml_editor and template_editor
    let yaml_content = yaml_editor.getSession().getValue();
    let jinja_content = template_editor.getSession().getValue();

    // Create a new XMLHttpRequest object for making an AJAX request
    var xhr = new XMLHttpRequest();
    // Configure the request to be: POST, JSON and add CRSF Token
    xhr.open('POST', '/templateFiller/ajax/generate-multiple-configs/', true); 
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // Include CSRF token -> using custom function to retrieve

    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            // Handle the successful response here
            // [...]
            console.log('Response:', this.responseText);
            var response = JSON.parse(this.responseText);

            generator_output = document.getElementById('generator-output')
            generator_output.style.color = SUCCESS_COLOR;
            generator_output.innerHTML = response.message ;
        }
    }
    xhr.send(JSON.stringify({yaml_content: yaml_content, jinja_content: jinja_content}));
    console.log("creating template")  
}


//================================== get a specified token =================================================================
// This function is a general-purpose utility for retrieving the value of a cookie given its name
// @param name -> specifies the name of the cooke to be retrieved
//
// Function used here to get CSRF token from cookies
function getCookie(name) {
    // Initialize cookieValue to null, to be returned if the cookie is not found
    let cookieValue = null;

    // Check if the document.cookie object exists and is not an empty string
    if (document.cookie && document.cookie !== '') {
       // Split document.cookie into individual cookies at each ';' and store in an array
        const cookies = document.cookie.split(';');

        // Iterate over each cookie in the array
        for (let i = 0; i < cookies.length; i++) {
            // Trim leading and trailing whitespace from the current cookie string
            const cookie = cookies[i].trim();

            // Check if the current cookie string starts with the name of the cookie being searched
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // If found, decode the cookie value using decodeURIComponent
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    // Return the value of the cookie, or null if not found
    return cookieValue;
}


//===================================== AJAX & JQuery Setup ==============================================================
// JQuery
// initialize jQuery for AJAX Request with CRSF Token
jQuery.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", jQuery('[name="csrfmiddlewaretoken"]').val());
        }
    }
});


//=========================================== jQuery - Run on DOM / Page finished loading ========================================================
jQuery(document).ready(function(){
    // when the document is loaded execute here 
    // [...]

    // run funciton when the Submit burron with the ID is clicked / submitted
    jQuery('#spreadsheet-input').submit(function(event){
        event.preventDefault();  // Prevent default form submission 

        message_box = document.getElementById('spreadsheet-message-box');

        // AJAX configuration for this specific element
        jQuery.ajax({
            type: 'POST',
            url: '/templateFiller/ajax/upload-excel/',  // URL to send the form data to
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function(response){
                // this code runs, when the AJAX request returns "success"
                // Handle success: update part of your page, show a message, etc.

                // display the message and change some CSS for added visuals
                document.getElementById('spreadsheet-submit-button').style.backgroundColor = SUCCESS_COLOR;
                message_box.innerHTML = response.message ;
                message_box.style.color = SUCCESS_COLOR;
                message_box.style.opacity = 1;
                document.getElementById('fill-multiple-template').disabled = false;
            },
            error: function(xhr, errmsg, err){
                // this code runs, when the AJAX request returns "error"
                // Handle error

                // display the message and change some CSS for added visuals
                document.getElementById('spreadsheet-submit-button').style.backgroundColor = ERROR_COLOR;
                message_box.innerHTML = errmsg;    
                message_box.style.color = ERROR_COLOR;
                message_box.style.opacity = 1;
            }
        });
    });
});












//=========================================== local code editing and testing functions ========================================================
function start_interval_timer()
{
    if (!JINJA_VARIABLE_INTERVAL_RUNNING)
    {
        JINJA_VARIABLE_INTERVAL = setInterval(find_jinja_variables, 1200);
        JINJA_VARIABLE_INTERVAL_RUNNING = true;
    }
}

function end_interval()
{
    // reset the timer, that would show the variables
    clearInterval(JINJA_VARIABLE_INTERVAL);
    JINJA_VARIABLE_INTERVAL_RUNNING = false;
}

// inital variables are shown
find_jinja_variables();
function find_jinja_variables()
{
    let jinja_content = template_editor.getSession().getValue();
    //let jinja_variables = jinja_content.match(REGEX_JINJA_VARIABLES);

    // Regular expression patterns for Jinja variables
    const patterns = [
        /\{\{\s*([a-zA-Z0-9.-_]+)\s*\}\}/g, // pattern for variables
        /{%[-]?\s*for\s+\w+\s+in\s+([a-zA-Z0-9.-_]+)\s*%}/g, // pattern for loop
        /\{\%\s*if\s+([\w\.]+)\s*\%\}|\{\%\s*if\s+\w+\s+in\s+([\w\.]+)\s*\%\}/g // pattern for if statement
    ];

    let allMatches = [];

    // Find all matches
    patterns.forEach(pattern => {
        let match;
        while ((match = pattern.exec(jinja_content)) !== null) {
            // Add the non-null capturing groups to allMatches
            allMatches = allMatches.concat(match.slice(1).filter(Boolean));
        }
    });
    JINJA_HELPER_FIELD.innerHTML = allMatches;
    end_interval()
    console.log(allMatches);
}

