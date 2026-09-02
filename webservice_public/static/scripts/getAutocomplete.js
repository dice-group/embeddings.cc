document.addEventListener("DOMContentLoaded", () => {
  const entityInput = document.getElementById("entity-input");
  const sourceInputs = document.querySelectorAll(
    'input[name="entity-source"]'
  );

  if (!entityInput || typeof autoComplete === "undefined") return;

  const autocompleteSources = new Set(["wikidata", "dbpedia"]);
  let activeRequest = null;
  let requestVersion = 0;

  function getSelectedSource() {
    return (
      document.querySelector('input[name="entity-source"]:checked')?.value ||
      "wdc"
    );
  }

  const autoCompleteJS = new autoComplete({
    selector: "#entity-input",
    threshold: 3,
    debounce: 300,
    data: {
      keys: ["label"],
      src: async (query) => {
        const source = getSelectedSource();
        if (!autocompleteSources.has(source)) return [];

        if (activeRequest) activeRequest.abort();
        const controller = new AbortController();
        activeRequest = controller;
        const currentRequestVersion = ++requestVersion;

        try {
          const response = await fetch(
            `/demo/autocomplete_sparql?source=${encodeURIComponent(
              source
            )}&search_term=${encodeURIComponent(query)}`,
            { signal: controller.signal }
          );

          if (!response.ok) throw new Error(response.statusText);
          const suggestions = await response.json();

          if (
            currentRequestVersion !== requestVersion ||
            source !== getSelectedSource()
          ) {
            return [];
          }

          return suggestions;
        } catch (error) {
          if (error.name !== "AbortError") {
            console.error("Failed to load autocomplete suggestions:", error);
          }
          return [];
        } finally {
          if (currentRequestVersion === requestVersion) activeRequest = null;
        }
      },
    },
    resultsList: {
      maxResults: 5,
    },
    resultItem: {
      highlight: true,
    },
    events: {
      input: {
        selection: (event) => {
          const selection = event.detail.selection.value;
          if (!selection || selection.source !== getSelectedSource()) return;

          autoCompleteJS.close();
          updateEntitySubmit(selection.entity);
        },
      },
    },
  });

  sourceInputs.forEach((input) => {
    input.addEventListener("change", () => {
      requestVersion += 1;
      if (activeRequest) activeRequest.abort();
      activeRequest = null;
      autoCompleteJS.close();
    });
  });
});
