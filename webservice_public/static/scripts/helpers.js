function updateEntitySubmit(entityText) {
  document.getElementById("entity-input").value = entityText;
  setEmbeddingsDomain(getDomainFromUri(entityText));
  document.getElementById("embed-btn").click();
}

const __domainColorCache = new Map();

function normalizeUri(raw) {
  if (typeof raw !== "string") return "";
  const s = raw.trim();
  return s;
}

function getDomainFromUri(raw) {
  const s = normalizeUri(raw);

  try {
    const hasScheme = /^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(s);
    const looksLikeHost = /^[\w.-]+\.[a-z]{2,}(\/|$)/i.test(s);

    if (!hasScheme && looksLikeHost) {
      return new URL("https://" + s).hostname.replace(/^www\./i, "");
    }

    const url = new URL(s);
    return (url.hostname || "").replace(/^www\./i, "");
  } catch (_) {
    return "";
  }
}

function hash32FNV1a(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function hueDist(a, b) {
  const d = Math.abs(a - b) % 360;
  return Math.min(d, 360 - d);
}

function domainToColors(domain) {
  if (!domain) return null;

  const cached = __domainColorCache.get(domain);
  if (cached) return cached;

  const seed = hash32FNV1a(domain);

  const SLOTS = 30;
  const hueOfSlot = (slot) => (slot * 360) / SLOTS;

  const used = Array.from(__domainColorCache.values())
    .filter((v) => v && Number.isFinite(v.slot))
    .map((v) => v.slot);

  const usedSet = new Set(used);
  const preferred = seed % SLOTS;

  let bestSlot = null;
  let bestScore = -1;
  let bestTie = Infinity;

  for (let s = 0; s < SLOTS; s++) {
    if (usedSet.has(s)) continue;

    const h = hueOfSlot(s);

    let minD = 9999;
    for (const us of used) minD = Math.min(minD, hueDist(h, hueOfSlot(us)));

    const tie = Math.min(
      Math.abs(s - preferred),
      SLOTS - Math.abs(s - preferred)
    );

    if (minD > bestScore || (minD === bestScore && tie < bestTie)) {
      bestScore = minD;
      bestTie = tie;
      bestSlot = s;
    }
  }

  if (bestSlot === null) bestSlot = preferred;

  const h = hueOfSlot(bestSlot);

  const sat = 62 + ((seed >>> 8) % 10);
  const light = 84 + ((seed >>> 16) % 7);

  const bg = `hsl(${h.toFixed(1)}, ${sat}%, ${light}%)`;
  const border = `hsl(${h.toFixed(1)}, ${sat}%, ${Math.max(30, light - 28)}%)`;

  const colors = { bg, border, slot: bestSlot };
  __domainColorCache.set(domain, colors);
  return colors;
}

function applyDomainColor(el, uri) {
  if (!el) return;

  const domain = getDomainFromUri(uri);
  if (!domain) return;

  const colors = domainToColors(domain);
  if (!colors) return;

  el.style.backgroundColor = colors.bg;
  el.style.borderColor = colors.border;
  el.dataset.domain = domain;
  el.title = domain;
}

function setEmbeddingsDomain(domain) {
  const el = document.getElementById("embed-domain");
  if (!el) return;

  if (!domain) {
    el.textContent = "";
    el.style.display = "none";
    return;
  }

  const colors = domainToColors(domain);
  el.textContent = domain;
  el.style.display = "inline-flex";

  if (colors) {
    el.style.backgroundColor = colors.bg;
    el.style.borderColor = colors.border;
  }
}
