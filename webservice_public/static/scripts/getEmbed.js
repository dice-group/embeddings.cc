document.addEventListener("DOMContentLoaded", () => {
  const embedBtn = document.getElementById("embed-btn");
  const entityInput = document.getElementById("entity-input");
  const embedOutput = document.getElementById("embeddings-output");
  const errorMsg = document.getElementById("error-message");

  if (embedBtn && entityInput && embedOutput) {
    embedBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      setEmbeddingsDomain(getDomainFromUri(entityInput.value));

      const origText = embedBtn.textContent;
      embedBtn.textContent = "Loading...";
      embedBtn.disabled = true;
      errorMsg.textContent = "";

      try {
        const resp = await fetch("/whale/embeddings", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ entity: entityInput.value }),
        });
        if (!resp.ok) throw new Error(resp.statusText);
        const { embeddings } = await resp.json();
        if (embeddings && embeddings.length) {
          embedOutput.style.display = "block";
          embedOutput.value = embeddings;
        } else {
          errorMsg.textContent =
            "No embeddings found for that entity. Please try another input.";
          errorMsg.style.display = "block";
        }
      } catch (err) {
        console.error("Failed to load embeddings:", err);
        errorMsg.textContent =
          "Error fetching embedding. Please try again later.";
        errorMsg.style.display = "block";
      } finally {
        embedBtn.textContent = origText;
        embedBtn.disabled = false;
      }
    });
  }
});
