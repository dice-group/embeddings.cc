document.addEventListener("DOMContentLoaded", () => {
  const embedBtn = document.getElementById("embed-btn");
  const entityInput = document.getElementById("entity-input");
  const embedOutput = document.getElementById("embeddings-output");
  const globalContainer = document.getElementById(
    "global-embeddings-container"
  );
  const globalOutput = document.getElementById("global-embeddings-output");
  const errorMsg = document.getElementById("error-message");

  if (embedBtn && entityInput && embedOutput && errorMsg) {
    embedBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      const entity = (entityInput.value || "").trim();
      setEmbeddingsDomain(getDomainFromUri(entity));

      const origText = embedBtn.textContent;
      embedBtn.textContent = "Loading...";
      embedBtn.disabled = true;
      errorMsg.textContent = "";
      errorMsg.style.display = "none";

      embedOutput.style.display = "none";
      embedOutput.value = "";
      if (globalContainer) globalContainer.style.display = "none";
      if (globalOutput) globalOutput.value = "";

      try {
        if (!entity) return;

        let localEmbeddings = [];
        try {
          const localResp = await fetch("/demo/embeddings", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({ entity, index: "local_demo" }),
          });

          if (localResp.ok) {
            const data = await localResp.json();
            localEmbeddings = (data && data.embeddings) || [];
          }
        } catch (_) {}

        if (localEmbeddings && localEmbeddings.length) {
          embedOutput.style.display = "block";
          embedOutput.value = localEmbeddings;

          let globalEmbeddings = [];
          try {
            const globalResp = await fetch("/demo/embeddings", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Accept: "application/json",
              },
              body: JSON.stringify({ entity, index: "global_demo" }),
            });

            if (globalResp.ok) {
              const data = await globalResp.json();
              globalEmbeddings = (data && data.embeddings) || [];
            }
          } catch (_) {}

          if (
            globalEmbeddings &&
            globalEmbeddings.length &&
            globalContainer &&
            globalOutput
          ) {
            globalContainer.style.display = "block";
            globalOutput.value = globalEmbeddings;
          } else if (globalContainer) {
            globalContainer.style.display = "none";
          }

          return;
        }

        const resp = await fetch("/whale/embeddings", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ entity }),
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
