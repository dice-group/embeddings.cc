document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("random-btn");
  const container = document.getElementById("random-entities");
  const randomError = document.getElementById("random-error-message");

  if (container) {
    container.querySelectorAll("span.entity").forEach((span) => {
      applyDomainColor(span, span.textContent);
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
        const resp = await fetch("/whale/random_uris");
        if (!resp.ok) throw new Error(resp.statusText);
        const { entities } = await resp.json();

        if (entities && entities.length) {
          container.innerHTML = "";
          entities.forEach((val) => {
            const span = document.createElement("span");
            span.className = "entity";
            span.textContent = val;
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
