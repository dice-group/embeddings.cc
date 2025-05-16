document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("get-embeddings-form");
  const textarea = document.getElementById("get_embeddings_parameters");
  const inputEl = document.getElementById("get_embeddings_input");
  const resultEl = document.getElementById("get_embeddings_result");
  const spinner = form.querySelector(".spinner");
  const submitBtn = form.querySelector('input[type="submit"]');

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    let userPayload;

    try {
      userPayload = JSON.parse(textarea.value);
    } catch (err) {
      inputEl.closest("tr").style.display = "none";
      resultEl.closest("tr").style.display = "table-row";
      resultEl.textContent = "Invalid JSON: " + err;
      return;
    }

    const payload = Array.isArray(userPayload)
      ? { entities: userPayload, index: "whale" }
      : { ...userPayload, index: "whale" };

    inputEl.textContent = JSON.stringify(payload, null, 2);
    inputEl.closest("tr").style.display = "table-row";
    Prism.highlightElement(inputEl);

    submitBtn.disabled = true;
    spinner.style.display = "inline-block";

    try {
      const response = await fetch(
        window.location.origin + "/api/v1/get_embeddings",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }
      const data = await response.json();
      console.log("fetched get_embeddings data:", data);

      let pretty;
      pretty = data.map((item) => JSON.stringify(item)).join("\n");

      resultEl.textContent = pretty;
    } catch (error) {
      resultEl.textContent = "Error: " + error.message;
    } finally {
      resultEl.closest("tr").style.display = "table-row";
      Prism.highlightElement(resultEl);
      submitBtn.disabled = false;
      spinner.style.display = "none";
    }
  });
});
