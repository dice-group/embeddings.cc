function apiCall(httpMethod, path, parameters, inputId, resultId) {
    var domain = window.location.origin;
    //var domain = 'https://embeddings.cc';
    var xhr = new XMLHttpRequest();
    xhr.open(httpMethod, domain + path, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function() {

        // Success
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {

            // Display input parameters
            if(inputId != null) {
                document.getElementById(inputId).parentElement.parentElement.parentElement.style.display = "table-row";
                if (path == '/api/v1/get_similar_embeddings') {
                    document.getElementById(inputId).innerHTML = JSON.stringify(parameters).replace(/\],\[/g,'\],\n\[').trim();
                } else {
                    document.getElementById(inputId).innerHTML = JSON.stringify(parameters, null, 2);
                }
                Prism.highlightElement(document.getElementById(inputId))
            }
            document.getElementById(resultId).parentElement.parentElement.parentElement.style.display = "table-row";

            // Display result
            if (path == '/api/v1/ping') {
                document.getElementById(resultId).innerHTML = xhr.responseText;
            } else if (path == '/api/v1/get_embeddings' || path == '/api/v1/get_similar_embeddings' || path == '/api/v1/get_similar_entities') {
                document.getElementById(resultId).innerHTML = JSON.stringify(JSON.parse(xhr.responseText)).replace(/\],\[/g,'\],\n\[').trim();
            } else {
                document.getElementById(resultId).innerHTML = JSON.stringify(JSON.parse(xhr.responseText), null, 2);
            }
            Prism.highlightElement(document.getElementById(resultId))

        // Error
        } else if (this.readyState === XMLHttpRequest.DONE) {
            //console.log(xhr.responseText);

            // Display input parameters
            if(inputId != null) {
                document.getElementById(inputId).parentElement.parentElement.parentElement.style.display = "table-row";
                document.getElementById(inputId).innerHTML = JSON.stringify(parameters, null, 2);
                Prism.highlightElement(document.getElementById(inputId))
            }

            // Display result
            document.getElementById(resultId).parentElement.parentElement.parentElement.style.display = "table-row";
            document.getElementById(resultId).innerHTML = 'Error: ' + xhr.responseText;

        // Interim
        } else {
            //console.log("[Not Done] " + xhr.responseText);
        }
    }
    xhr.send(JSON.stringify(parameters));
}

function apiCallParse(httpMethod, path, parameterName, parametersId, inputId, resultId) {
    try {
        value = JSON.parse(document.getElementById(parametersId).value);
        return apiCall(httpMethod, path, {[parameterName]:value}, inputId, resultId)
    } catch (error) {
        document.getElementById(inputId).parentElement.parentElement.parentElement.style.display = "none";
        document.getElementById(resultId).parentElement.parentElement.parentElement.style.display = "table-row";
        document.getElementById(resultId).innerHTML = error;
    }    
}

function initialize_parameters(httpMethod, path, parameters) {
    var domain = window.location.origin;
    //var domain = 'https://embeddings.cc'
    var xhr = new XMLHttpRequest();
    xhr.open(httpMethod, domain + path, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            if (path == '/api/v1/get_random_entities') {
                document.getElementById('get_embeddings_parameters').innerHTML = xhr.responseText;
                document.getElementById('get_similar_entities_parameters').innerHTML = xhr.responseText;
                initialize_parameters('POST', '/api/v1/get_embeddings', {entities:JSON.parse(xhr.responseText)})
            } else if (path == '/api/v1/get_embeddings') {
                var embeddings = [];
                JSON.parse(xhr.responseText).forEach(element => embeddings.push(element[1]));
                document.getElementById('get_similar_embeddings_parameters').innerHTML = JSON.stringify(embeddings).replace(/\],\[/g,'\],\n\[').trim();
            }
        } else if (this.readyState === XMLHttpRequest.DONE) {
            console.log(xhr.responseText);
        } 
    }
    xhr.send(JSON.stringify(parameters));
}
