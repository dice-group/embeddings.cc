const PREDICT_ENDPOINT = "/predict";
const CLASS_EXAMPLES_ENDPOINT = "/class-examples";
const ENTITY_DETAILS_ENDPOINT = "/demo/dbpedia/entities";
const entityMetadata = new Map();

function stripQuotes(value) {
  return String(value).trim().replace(/^["']|["']$/g, "");
}

function parseUriList(value) {
  return value
    .split(/\r?\n/)
    .map(stripQuotes)
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

function createExampleList(kind) {
  const input = document.getElementById(`${kind}-examples`);
  const list = document.getElementById(`${kind}-example-list`);
  const status = document.getElementById(`${kind}-metadata-status`);
  let entries = [];
  let version = 0;
  let searchVersion = 0;
  let searchController = null;
  let autocomplete = null;

  function render() {
    list.replaceChildren();
    for (const entry of entries) {
      const metadata = entityMetadata.get(entry.uri);
      const row = document.createElement("li");
      const details = document.createElement("div");
      const label = document.createElement("span");
      label.className = "predict-entity-label";
      label.textContent = metadata?.label || entry.uri;
      label.title = entry.uri;
      details.append(label);
      const types = Array.isArray(metadata?.types)
        ? metadata.types.join(", ") : metadata?.types;
      if (types) {
        const typeText = document.createElement("span");
        typeText.className = "predict-entity-types";
        typeText.textContent = types;
        details.append(typeText);
      }
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "predict-entity-remove";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove ${metadata?.label || entry.uri}`);
      remove.addEventListener("click", () => {
        entries = entries.filter((item) => item !== entry);
        render();
        input.focus();
      });
      row.append(details, remove);
      list.append(row);
    }
  }

  async function resolveMetadata() {
    const currentVersion = ++version;
    const missing = entries.map((entry) => entry.uri)
      .filter((uri) => !entityMetadata.has(uri));
    status.textContent = missing.length ? "Loading labels and types…" : "";
    try {
      for (let offset = 0; offset < missing.length; offset += 500) {
        const response = await fetch(ENTITY_DETAILS_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ uris: missing.slice(offset, offset + 500) }),
        });
        if (!response.ok) throw new Error("Metadata lookup failed");
        const data = await response.json();
        if (!Array.isArray(data)) throw new Error("Invalid metadata response");
        for (const item of data) entityMetadata.set(item.entity, item);
        if (currentVersion !== version) return;
        render();
      }
      if (currentVersion === version) {
        status.textContent = entries.some((entry) => !entityMetadata.get(entry.uri)?.label)
          ? "Some labels are unavailable; their URIs will still be used." : "";
      }
    } catch {
      if (currentVersion === version) {
        status.textContent = "Labels could not be loaded. You can still predict using these URIs.";
      }
    }
  }

  function add(uris) {
    const seen = new Set(entries.map((entry) => entry.uri));
    for (const uri of uris) {
      if (!seen.has(uri)) {
        entries.push({ uri });
        seen.add(uri);
      }
    }
    render();
    void resolveMetadata();
  }

  function clearInput() {
    input.value = "";
    searchVersion += 1;
    searchController?.abort();
    autocomplete?.close();
  }

  function commitInput() {
    const uris = parseUriList(input.value);
    if (!uris.length) return;
    if (!uris.every((uri) => /^https?:\/\/\S+$/i.test(uri))) {
      throw new Error(`Select a DBpedia suggestion or enter a URI for ${kind} examples.`);
    }
    add(uris);
    clearInput();
  }

  input.addEventListener("paste", (event) => {
    const pasted = event.clipboardData?.getData("text") || "";
    const uris = parseUriList(pasted);
    if (uris.length && uris.every((uri) => /^https?:\/\/\S+$/i.test(uri))) {
      event.preventDefault();
      add(uris);
      clearInput();
    }
  });
  input.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    if (/^https?:\/\/\S+$/i.test(stripQuotes(input.value))) {
      commitInput();
    }
  });
  input.addEventListener("blur", () => {
    if (/^https?:\/\/\S+$/i.test(stripQuotes(input.value))) commitInput();
  });

  if (typeof autoComplete !== "undefined") {
    autocomplete = new autoComplete({
      selector: `#${kind}-examples`,
      threshold: 3,
      debounce: 300,
      searchEngine: (query, record) => record,
      data: {
        keys: ["label"],
        src: async (query) => {
          searchController?.abort();
          const currentVersion = ++searchVersion;
          const controller = new AbortController();
          searchController = controller;
          if (/^https?:\/\//i.test(query)) return [];
          try {
            const response = await fetch(
              `/demo/autocomplete_sparql?source=dbpedia&search_term=${encodeURIComponent(query)}`,
              { signal: controller.signal }
            );
            if (!response.ok) return [];
            const data = await response.json();
            return currentVersion === searchVersion && input.value === query ? data : [];
          } catch {
            return [];
          }
        },
      },
      resultsList: { maxResults: 5 },
      resultItem: {
        element: (item, data) => {
          const suggestion = data.value;
          const types = Array.isArray(suggestion.types)
            ? suggestion.types.join(", ") : suggestion.types;
          item.textContent = types ? `${suggestion.label} — ${types}` : suggestion.label;
        },
      },
      events: {
        input: {
          selection: (event) => {
            const selected = event.detail.selection.value;
            entityMetadata.set(selected.entity, selected);
            add([selected.entity]);
            clearInput();
          },
        },
      },
    });
  }

  return {
    uris: () => entries.map((entry) => entry.uri),
    commitInput,
    replace: (uris) => {
      entries = [];
      clearInput();
      add(uris.map(stripQuotes).filter(Boolean));
    },
  };
}

const positiveExamples = createExampleList("positive");
const negativeExamples = createExampleList("negative");
const exampleCount = document.getElementById("example-count");
const exampleCountValue = document.getElementById("example-count-value");

function updateExampleCount() {
  exampleCountValue.value = exampleCount.value;
  const progress = (exampleCount.value - exampleCount.min) / (exampleCount.max - exampleCount.min);
  exampleCount.style.setProperty("--slider-fill", `${progress * 100}%`);
}

exampleCount.addEventListener("input", updateExampleCount);
updateExampleCount();

document.getElementById("random-example-btn").addEventListener("click", async () => {
  const randomButton = document.getElementById("random-example-btn");
  const predictButton = document.getElementById("predict-btn");
  const errorMessage = document.getElementById("predict-error-message");
  const exampleExpressionContainer = document.getElementById("example-expression-container");
  const exampleExpression = document.getElementById("example-expression");
  const resultContainer = document.getElementById("predict-result-container");
  const expression = document.getElementById("predict-expression");
  const f1 = document.getElementById("predict-f1");
  const originalText = randomButton.textContent;

  errorMessage.textContent = "";
  exampleExpression.textContent = "";
  exampleExpressionContainer.style.display = "none";
  expression.textContent = "";
  f1.textContent = "";
  resultContainer.style.display = "none";
  randomButton.textContent = "Loading...";
  randomButton.disabled = true;
  predictButton.disabled = true;

  try {
    const response = await fetch(`${CLASS_EXAMPLES_ENDPOINT}?count=${encodeURIComponent(exampleCount.value)}`);
    const data = await readResponseBody(response);

    if (!response.ok) {
      throw new Error(data.detail ? renderValue(data.detail) : renderError(data, response.status));
    }

    positiveExamples.replace(data.positive_uris || []);
    negativeExamples.replace(data.negative_uris || []);
    exampleExpression.textContent = renderValue(data.expression);
    exampleExpressionContainer.style.display = "block";
  } catch (error) {
    errorMessage.textContent = error.message || "Could not get a random example.";
  } finally {
    randomButton.textContent = originalText;
    randomButton.disabled = false;
    predictButton.disabled = false;
  }
});

document.getElementById("predict-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  const button = document.getElementById("predict-btn");
  const randomButton = document.getElementById("random-example-btn");
  const errorMessage = document.getElementById("predict-error-message");
  const resultContainer = document.getElementById("predict-result-container");
  const expression = document.getElementById("predict-expression");
  const f1 = document.getElementById("predict-f1");
  const origText = button.textContent;

  errorMessage.textContent = "";
  expression.textContent = "";
  f1.textContent = "";
  resultContainer.style.display = "none";
  button.textContent = "Loading...";
  button.disabled = true;
  randomButton.disabled = true;

  try {
    positiveExamples.commitInput();
    negativeExamples.commitInput();
    const payload = {
      positive_uris: positiveExamples.uris(),
      negative_uris: negativeExamples.uris(),
    };

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
    f1.textContent = renderValue(data.f1);
    resultContainer.style.display = "block";
  } catch (error) {
    errorMessage.textContent = error.message || "Prediction failed.";
  } finally {
    button.textContent = origText;
    button.disabled = false;
    randomButton.disabled = false;
  }
});
