console.log("templateFiller.js")

//let fill_template_button = document.getElementById("fill-template")

// deprecated with ACE editor
//let yaml_input = document.getElementById("yaml-input");
//let jinja_template_input = document.getElementById("jinja-template-input");

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('fill-template').addEventListener('click', create_config_from_template);
});

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