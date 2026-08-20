document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("random-btn");
  const container = document.getElementById("random-entities");
  const randomError = document.getElementById("random-error-message");
  const sourceInputs = document.querySelectorAll(
    'input[name="entity-source"]'
  );
  const defaultBtnText = btn ? btn.textContent : "";
  let activeRequest = null;
  let requestVersion = 0;

  function resetRandomEntities() {
    requestVersion += 1;
    if (activeRequest) activeRequest.abort();
    activeRequest = null;

    if (container) container.innerHTML = "";
    if (randomError) {
      randomError.textContent = "";
      randomError.style.display = "none";
    }
    if (btn) {
      btn.textContent = defaultBtnText;
      btn.disabled = false;
    }
  }

  sourceInputs.forEach((input) => {
    input.addEventListener("change", resetRandomEntities);
  });

  if (container) {
    container.querySelectorAll("span.entity").forEach((span) => {
      const entity = span.dataset.entity || span.textContent.trim();
      span.dataset.entity = entity;
      span.textContent = decodeEntityUriForDisplay(entity);
      span.onclick = () => updateEntitySubmit(entity);
      applyDomainColor(span, entity);
    });
  }

  if (btn && container && randomError) {
    btn.addEventListener("click", async function (e) {
      e.preventDefault();

      if (activeRequest) activeRequest.abort();
      const controller = new AbortController();
      activeRequest = controller;
      const currentRequestVersion = ++requestVersion;

      btn.textContent = "Loading...";
      btn.disabled = true;
      randomError.textContent = "";
      randomError.style.display = "none";

      try {
        const selectedSource =
          document.querySelector('input[name="entity-source"]:checked')
            ?.value || "wdc";
        const endpoint =
          selectedSource === "wdc"
            ? "/demo/random_uris_global"
            : `/demo/random_uris_sparql?source=${encodeURIComponent(
                selectedSource
              )}`;

        const resp = await fetch(endpoint, { signal: controller.signal });
        if (!resp.ok) throw new Error(resp.statusText);
        const { entities } = await resp.json();

        if (currentRequestVersion !== requestVersion) return;

        if (entities && entities.length) {
          container.innerHTML = "";
          entities.forEach((val) => {
            const span = document.createElement("span");
            span.className = "entity";
            span.dataset.entity = val;
            span.textContent = decodeEntityUriForDisplay(val);
            span.onclick = () => updateEntitySubmit(val);

            applyDomainColor(span, val);

            container.appendChild(span);
          });
        } else {
          randomError.textContent =
            "No entities found. Please try again later.";
          randomError.style.display = "block";
        }
      } catch (err) {
        if (
          err.name === "AbortError" ||
          currentRequestVersion !== requestVersion
        )
          return;
        console.error("Failed to load entites:", err);
        randomError.textContent =
          "Error fetching entites. Please try again later.";
        randomError.style.display = "block";
      } finally {
        if (currentRequestVersion === requestVersion) {
          activeRequest = null;
          btn.textContent = defaultBtnText;
          btn.disabled = false;
        }
      }
    });
  }
});
