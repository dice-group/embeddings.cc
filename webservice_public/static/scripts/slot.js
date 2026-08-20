document.addEventListener("DOMContentLoaded", () => {
  const slot = document.getElementById("slot-machine");
  const countEl = document.getElementById("count");
  const loops = 3;
  let strips = [];
  let currentLen = 0;
  let digitH = 0;

  let previousPlain = null;

  function formatCompactCount(value) {
    if (!Number.isFinite(value)) return "—";
    if (value >= 1_000_000_000) {
      return `${(value / 1_000_000_000).toFixed(1).replace(/\.0$/, "")}B`;
    }
    if (value >= 1_000_000) {
      return `${Math.round(value / 1_000_000)}M`;
    }
    return new Intl.NumberFormat("en-US").format(value);
  }

  function updateSourceCounts(sourceCounts) {
    document.querySelectorAll("[data-source-count]").forEach((element) => {
      const value = Number(sourceCounts?.[element.dataset.sourceCount]);
      element.textContent = formatCompactCount(value);
    });
  }

  function initReels(n) {
    slot.innerHTML = "";
    strips = [];
    currentLen = n;

    for (let i = 0; i < n; i++) {
      const reel = document.createElement("div");
      reel.className = "reel";
      const strip = document.createElement("div");

      for (let cycle = 0; cycle < loops + 1; cycle++) {
        for (let d = 0; d <= 9; d++) {
          const cell = document.createElement("div");
          cell.textContent = d;
          strip.appendChild(cell);
        }
      }

      reel.appendChild(strip);
      slot.appendChild(reel);
      strips.push(strip);

      if ((n - i - 1) % 3 === 0 && i !== n - 1) {
        const comma = document.createElement("div");
        comma.className = "delimiter";
        comma.textContent = ",";
        slot.appendChild(comma);
      }
    }

    digitH = strips[0].firstElementChild.offsetHeight;
    slot.querySelectorAll(".reel").forEach((r) => {
      r.style.height = digitH + "px";
    });

    strips.forEach((strip) => {
      Array.from(strip.children).forEach((cell) => {
        cell.style.height = digitH + "px";
        cell.style.lineHeight = digitH + "px";
        cell.style.display = "flex";
        cell.style.alignItems = "center";
        cell.style.justifyContent = "center";
      });
    });

    strips.forEach((strip) => {
      strip.currentDigit = 0;
      strip.style.transition = "transform 1s ease-in-out";
      strip.style.transform = "translateY(0)";

      strip.addEventListener("transitionend", (e) => {
        if (e.propertyName !== "transform") return;

        strip.style.transition = "none";
        strip.style.transform = `translateY(${-strip.currentDigit * digitH}px)`;
        strip.offsetHeight;
        strip.style.transition = "transform 1s ease-in-out";

        if (strip === strips[strips.length - 1]) {
          slot.style.display = "none";
          countEl.style.display = "inline";
        }
      });
    });
  }

  function updateCount() {
    fetch("/whale/count")
      .then((r) => {
        if (!r.ok) throw new Error(r.statusText);
        return r.json();
      })
      .then((data) => {
        if (data.count == null) throw new Error("Count unavailable");
        updateSourceCounts(data.sources);
        const real = data.count;
        const plain = new Intl.NumberFormat("en-US", {
          useGrouping: false,
        }).format(real);

        if (plain === previousPlain) {
          const formatted = new Intl.NumberFormat("en-US").format(real);
          countEl.innerHTML = formatted.replace(
            /,/g,
            '<span class="delimiter">,</span>'
          );
          slot.style.display = "none";
          countEl.style.display = "inline";
          return;
        }

        if (plain.length !== currentLen) {
          initReels(plain.length);
        }

        let diffIndex = 0;
        if (previousPlain) {
          while (
            diffIndex < plain.length &&
            diffIndex < previousPlain.length &&
            plain[diffIndex] === previousPlain[diffIndex]
          ) {
            diffIndex++;
          }
        }

        const formatted = new Intl.NumberFormat("en-US").format(real);
        countEl.innerHTML = formatted.replace(
          /,/g,
          '<span class="delimiter">,</span>'
        );

        slot.style.display = "inline-flex";
        countEl.style.display = "none";

        for (let i = 0; i < diffIndex; i++) {
          const d = +plain[i];
          const strip = strips[i];
          strip.currentDigit = d;
          strip.style.transition = "none";
          strip.style.transform = `translateY(${-d * digitH}px)`;
        }

        slot.offsetHeight;

        plain.split("").forEach((ch, i) => {
          if (i < diffIndex) return;
          const d = +ch;
          const strip = strips[i];
          const offset = -(loops * 10 + d) * digitH;

          strip.currentDigit = d;
          strip.style.transition = "transform 1s ease-in-out";
          strip.style.transform = `translateY(${offset}px)`;
        });

        setTimeout(() => {
          slot.style.display = "none";
          countEl.style.display = "inline";
        }, 1000);

        previousPlain = plain;
      })
      .catch(() => {
        updateSourceCounts({});
        slot.style.display = "none";
        countEl.style.display = "inline";
        countEl.textContent = "MILLIONS";
      });
  }

  updateCount();
});
