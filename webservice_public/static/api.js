function apiCall(formEl, httpMethod, path, parameters, inputId, resultId) {
  var domain = window.location.origin;
  //var domain = 'https://embeddings.cc';

  var submitBtn = formEl.querySelector('input[type="submit"]');
  var spinner = formEl.querySelector(".spinner");

  submitBtn.disabled = true;
  spinner.style.display = "inline-block";

  var xhr = new XMLHttpRequest();
  xhr.open(httpMethod, domain + path, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    // Success
    if (xhr.readyState !== XMLHttpRequest.DONE) {
      return;
    }

    submitBtn.disabled = false;
    spinner.style.display = "none";

    if (xhr.status === 200) {
      // Display input parameters
      if (inputId != null) {
        const inEl = document.getElementById(inputId);
        inEl.parentElement.parentElement.parentElement.style.display =
          "table-row";
        if (path == "/api/v1/get_similar_embeddings") {
          inEl.textContent = JSON.stringify(parameters).replace(
            /\],\[/g,
            "],\n["
          );
        } else {
          inEl.textContent = JSON.stringify(parameters, null, 2);
        }
        Prism.highlightElement(inEl);
      }

      const outRow =
        document.getElementById(resultId).parentElement.parentElement
          .parentElement;
      outRow.style.display = "table-row";

      const outEl = document.getElementById(resultId);

      // Display result
      if (path == "/api/v1/ping") {
        outEl.textContent = xhr.responseText;
      } else {
        const parsed = JSON.parse(xhr.responseText);
        let pretty;
        if (
          [
            "/api/v1/get_embeddings",
            "/api/v1/get_similar_embeddings",
            "/api/v1/get_similar_entities",
          ].includes(path)
        ) {
          pretty = JSON.stringify(parsed).replace(/\],\[/g, "],\n[");
        } else {
          pretty = JSON.stringify(parsed, null, 2);
        }
        outEl.textContent = pretty;
      }
      Prism.highlightElement(outEl);
    } else {
      // Display input parameters
      if (inputId) {
        const inEl = document.getElementById(inputId);
        inEl.parentElement.parentElement.parentElement.style.display =
          "table-row";
        inEl.textContent = JSON.stringify(parameters, null, 2);
        Prism.highlightElement(inEl);
      }

      // Display result
      const outRow =
        document.getElementById(resultId).parentElement.parentElement
          .parentElement;
      outRow.style.display = "table-row";
      document.getElementById(resultId).textContent =
        "Error: " + xhr.responseText;

      // Interim
    }
  };
  xhr.send(JSON.stringify(parameters));

  return false;
}

function apiCallParse(
  formEl,
  httpMethod,
  path,
  parameterName,
  parametersId,
  inputId,
  resultId
) {
  let raw;
  try {
    raw = document.getElementById(parametersId).value;
  } catch (err) {
    console.error("No element with id=", parametersId);
    return false;
  }

  let value;
  try {
    value = JSON.parse(raw);
  } catch (error) {
    document.getElementById(inputId).closest("tr").style.display = "none";

    document.getElementById(resultId).closest("tr").style.display = "table-row";
    document.getElementById(resultId).textContent = "Invalif JSON:" + error;
    return false;
  }

  const params = { [parameterName]: value };

  return apiCall(formEl, httpMethod, path, params, inputId, resultId);
}

function initialize_parameters(httpMethod, path, parameters) {
  var domain = window.location.origin;
  //var domain = 'https://embeddings.cc'
  var xhr = new XMLHttpRequest();
  xhr.open(httpMethod, domain + path, true);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.onreadystatechange = function () {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      if (path == "/api/v1/get_random_entities") {
        document.getElementById("get_embeddings_parameters").innerHTML =
          xhr.responseText;
        document.getElementById("get_similar_entities_parameters").innerHTML =
          xhr.responseText;
        initialize_parameters("POST", "/api/v1/get_embeddings", {
          entities: JSON.parse(xhr.responseText),
        });
      } else if (path == "/api/v1/get_embeddings") {
        var embeddings = [];
        JSON.parse(xhr.responseText).forEach((element) =>
          embeddings.push(element[1])
        );
        document.getElementById("get_similar_embeddings_parameters").innerHTML =
          JSON.stringify(embeddings).replace(/\],\[/g, "],\n[").trim();
      }
    } else if (this.readyState === XMLHttpRequest.DONE) {
      console.log(xhr.responseText);
    }
  };
  xhr.send(JSON.stringify(parameters));
}
