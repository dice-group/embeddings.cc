document.addEventListener("DOMContentLoaded", () => {
  initialize_parameters("POST", "/api/v1/get_random_entities", { size: "2" });

  fetch(window.location.origin + "/api/v1/get_random_entities", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index: "whale", size: "2" }),
  })
    .then((response) => {
      if (!response.ok) throw new Error(response.statusText);
      return response.json();
    })
    .then((ids) => {
      const payload = { index: "whale", entities: ids };
      const el = document.getElementById("get_embeddings_parameters");
      el.textContent = JSON.stringify(payload, null, 2);
      Prism.highlightElement(el);
    })
    .catch(console.error);
});
