document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("random-btn");
  const container = document.getElementById("random-entities");
  const randomError = document.getElementById("random-error-message");

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

      const originalText = btn.textContent;
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

        const resp = await fetch(endpoint);
        if (!resp.ok) throw new Error(resp.statusText);
        const { entities } = await resp.json();

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
        console.error("Failed to load entites:", err);
        randomError.textContent =
          "Error fetching entites. Please try again later.";
        randomError.style.display = "block";
      } finally {
        btn.textContent = originalText;
        btn.disabled = false;
      }
    });
  }
});
