document.addEventListener("DOMContentLoaded", () => {
  const cache = {};

  function debounce(fn, wait = 300) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      return new Promise((resolve) => {
        timeout = setTimeout(async () => {
          resolve(await fn(...args));
        }, wait);
      });
    };
  }

  const _fetch = async (query) => {
    const res = await fetch(
      `/autocomplete?search_term=${encodeURIComponent(query)}&index=whale`
    );
    return res.ok ? await res.json() : [];
  };

  const fetchSuggestions = debounce(async (query) => {
    if (cache[query]) {
      return cache[query];
    }
    try {
      const json = await _fetch(query);
      cache[query] = json;
      return json;
    } catch {
      return [];
    }
  }, 300);

  const autoCompleteEntity = new autoComplete({
    selector: "#entity-input",
    placeHolder: "Search for embeddings...",
    threshold: 3,
    debounce: 0,
    data: {
      src: async (query) => {
        if (query.length < 3) return [];
        return await fetchSuggestions(query);
      },
    },
    resultItem: {
      highlight: true,
    },
    events: {
      input: {
        selection: (event) => {
          console.log("AC selection event:", event);
          autoCompleteEntity.input.value = event.detail.selection.value;
          document.getElementById("embed-btn").click();
        },
      },
    },
  });

  const wrapper = document.querySelector(".autoComplete_wrapper");
  if (wrapper) wrapper.style.display = "inline-block";
});
