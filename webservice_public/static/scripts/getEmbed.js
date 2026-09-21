document.addEventListener("DOMContentLoaded", () => {
  const embedBtn = document.getElementById("embed-btn");
  const entityInput = document.getElementById("entity-input");
  const embedOutput = document.getElementById("embeddings-output");
  const globalContainer = document.getElementById(
    "global-embeddings-container"
  );
  const globalOutput = document.getElementById("global-embeddings-output");
  const errorMsg = document.getElementById("error-message");
  const localLabel = document.getElementById("local-embeddings-label");
  const sourceInputs = document.querySelectorAll(
    'input[name="entity-source"]'
  );
  const defaultBtnText = embedBtn ? embedBtn.textContent : "";
  let activeRequest = null;
  let requestVersion = 0;

  function resetEmbeddings() {
    requestVersion += 1;
    if (activeRequest) activeRequest.abort();
    activeRequest = null;

    if (entityInput) entityInput.value = "";
    setEmbeddingsDomain("");
    if (embedOutput) {
      embedOutput.value = "";
      embedOutput.style.display = "none";
    }
    if (localLabel) localLabel.style.display = "none";
    if (globalOutput) globalOutput.value = "";
    if (globalContainer) globalContainer.style.display = "none";
    if (errorMsg) {
      errorMsg.textContent = "";
      errorMsg.style.display = "none";
    }
    if (embedBtn) {
      embedBtn.textContent = defaultBtnText;
      embedBtn.disabled = false;
    }
  }

  sourceInputs.forEach((input) => {
    input.addEventListener("change", resetEmbeddings);
  });

  if (embedBtn && entityInput && embedOutput && errorMsg) {
    embedBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      if (activeRequest) activeRequest.abort();
      const controller = new AbortController();
      activeRequest = controller;
      const currentRequestVersion = ++requestVersion;

      const entity = (entityInput.value || "").trim();
      const selectedSource =
        document.querySelector('input[name="entity-source"]:checked')
          ?.value || "wdc";
      setEmbeddingsDomain(getDomainFromUri(entity));

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

        if (selectedSource !== "wdc") {
          const sparqlResp = await fetch("/demo/embeddings_sparql", {
            method: "POST",
            signal: controller.signal,
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({ entity, source: selectedSource }),
          });
          if (!sparqlResp.ok) throw new Error(sparqlResp.statusText);

          const data = await sparqlResp.json();
          if (currentRequestVersion !== requestVersion) return;
          const embeddings = (data && data.embeddings) || [];
          if (embeddings.length) {
            embedOutput.style.display = "block";
            embedOutput.value = embeddings;
          } else {
            errorMsg.textContent =
              "No embeddings found for that entity. Please try another input.";
            errorMsg.style.display = "block";
          }
          return;
        }

        let localEmbeddings = [];
        try {
          const localResp = await fetch("/demo/embeddings", {
            method: "POST",
            signal: controller.signal,
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

        if (
          controller.signal.aborted ||
          currentRequestVersion !== requestVersion
        )
          return;

        if (localEmbeddings && localEmbeddings.length) {
          embedOutput.style.display = "block";
          embedOutput.value = localEmbeddings;

          let globalEmbeddings = [];
          try {
            const globalResp = await fetch("/demo/embeddings", {
              method: "POST",
              signal: controller.signal,
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
            controller.signal.aborted ||
            currentRequestVersion !== requestVersion
          )
            return;

          if (
            globalEmbeddings &&
            globalEmbeddings.length &&
            globalContainer &&
            globalOutput
          ) {
            if (localLabel)
              localLabel.style.setProperty("display", "block", "important");

            globalContainer.style.display = "block";
            globalOutput.value = globalEmbeddings;
          } else if (globalContainer) {
            if (localLabel) localLabel.style.display = "none";
            globalContainer.style.display = "none";
          }

          return;
        }

        const resp = await fetch("/whale/embeddings", {
          method: "POST",
          signal: controller.signal,
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ entity }),
        });
        if (!resp.ok) throw new Error(resp.statusText);
        const { embeddings } = await resp.json();
        if (currentRequestVersion !== requestVersion) return;
        if (embeddings && embeddings.length) {
          embedOutput.style.display = "block";
          embedOutput.value = embeddings;
        } else {
          errorMsg.textContent =
            "No embeddings found for that entity. Please try another input.";
          errorMsg.style.display = "block";
        }
      } catch (err) {
        if (
          err.name === "AbortError" ||
          currentRequestVersion !== requestVersion
        )
          return;
        console.error("Failed to load embeddings:", err);
        errorMsg.textContent =
          "Error fetching embedding. Please try again later.";
        errorMsg.style.display = "block";
      } finally {
        if (currentRequestVersion === requestVersion) {
          activeRequest = null;
          embedBtn.textContent = defaultBtnText;
          embedBtn.disabled = false;
        }
      }
    });
  }
});
