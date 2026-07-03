const PREDICT_ENDPOINT = "/predict";

function parseUriList(value) {
  return value
    .split(/\r?\n/)
    .map((item) => item.trim().replace(/^["']|["']$/g, ""))
    .filter(Boolean);
}

function renderValue(value) {
  if (value === null || value === undefined) {
    return "";
  }

  if (typeof value === "object" && typeof value.detail === "string") {
    return value.detail;
  }

  if (typeof value === "object") {
    return JSON.stringify(value, null, 2);
  }

  return String(value);
}

function renderError(errorData, responseStatus) {
  const parts = [];

  if (errorData.error) {
    parts.push(errorData.error);
  }

  if (errorData.status_code) {
    parts.push(`Upstream status: ${errorData.status_code}`);
  }

  if (errorData.detail !== null && errorData.detail !== undefined) {
    parts.push(`Detail: ${renderValue(errorData.detail)}`);
  }

  if (parts.length === 0) {
    parts.push(`Prediction failed with status ${responseStatus}`);
  }

  return parts.join("\n");
}

async function readResponseBody(response) {
  const text = await response.text();

  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch {
    return { detail: text };
  }
}

document.getElementById("predict-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const button = document.getElementById("predict-btn");
  const errorMessage = document.getElementById("predict-error-message");
  const resultContainer = document.getElementById("predict-result-container");
  const expression = document.getElementById("predict-expression");
  const rawOutput = document.getElementById("predict-raw-output");
  const parsesAsDl = document.getElementById("predict-parses-as-dl");
  const usedFallback = document.getElementById("predict-used-fallback");
  const origText = button.textContent;

  errorMessage.textContent = "";
  expression.textContent = "";
  rawOutput.textContent = "";
  parsesAsDl.textContent = "";
  usedFallback.textContent = "";
  resultContainer.style.display = "none";
  button.textContent = "Loading...";
  button.disabled = true;

  const payload = {
    positive_uris: parseUriList(document.getElementById("positive-examples").value),
    negative_uris: parseUriList(document.getElementById("negative-examples").value),
  };

  try {
    const response = await fetch(PREDICT_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await readResponseBody(response);
      throw new Error(errorData.detail ? renderValue(errorData.detail) : renderError(errorData, response.status));
    }

    const data = await readResponseBody(response);
    expression.textContent = renderValue(data.expression);
    rawOutput.textContent = renderValue(data.raw_output);
    parsesAsDl.textContent = renderValue(data.parses_as_dl);
    usedFallback.textContent = renderValue(data.used_fallback);
    resultContainer.style.display = "block";
  } catch (error) {
    errorMessage.textContent = error.message || "Prediction failed.";
  } finally {
    button.textContent = origText;
    button.disabled = false;
  }
});
