JS = r"""
(function () {
  "use strict";
  const root = document.documentElement;
  const memStore = {};

  /* ============ Persistent storage with graceful fallback ============ */
  async function storeGet(key) {
    try {
      if (window.storage && typeof window.storage.get === "function") {
        const r = await window.storage.get(key, false);
        return r ? r.value : null;
      }
    } catch (e) { /* key not found or storage unavailable */ }
    return Object.prototype.hasOwnProperty.call(memStore, key) ? memStore[key] : null;
  }
  async function storeSet(key, value) {
    memStore[key] = value;
    try {
      if (window.storage && typeof window.storage.set === "function") {
        await window.storage.set(key, value, false);
      }
    } catch (e) { /* ignore, in-memory fallback already set */ }
  }

  /* ============ Theme toggle ============ */
  const themeBtn = document.getElementById("theme-toggle");
  async function initTheme() {
    let saved = await storeGet("cy-guide-theme");
    if (!saved) {
      saved = (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
    }
    root.setAttribute("data-theme", saved);
  }
  initTheme();
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
      const next = current === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      storeSet("cy-guide-theme", next);
    });
  }

  /* ============ Reading progress bar ============ */
  const progressBar = document.getElementById("progress-bar");
  function updateProgress() {
    const h = document.documentElement;
    const scrollTop = h.scrollTop || document.body.scrollTop;
    const scrollHeight = (h.scrollHeight || document.body.scrollHeight) - h.clientHeight;
    const pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    if (progressBar) progressBar.style.width = pct + "%";
  }
  document.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  /* ============ Back to top ============ */
  const backBtn = document.getElementById("back-to-top");
  function updateBackBtn() {
    if (!backBtn) return;
    if (window.scrollY > 480) backBtn.classList.add("show");
    else backBtn.classList.remove("show");
  }
  document.addEventListener("scroll", updateBackBtn, { passive: true });
  if (backBtn) {
    backBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ============ Mobile sidebar ============ */
  const sidebar = document.querySelector("aside.sidebar");
  const menuToggle = document.getElementById("menu-toggle");
  const overlay = document.getElementById("overlay-backdrop");
  function openSidebar() { if (sidebar) sidebar.classList.add("open"); if (overlay) overlay.classList.add("show"); }
  function closeSidebar() { if (sidebar) sidebar.classList.remove("open"); if (overlay) overlay.classList.remove("show"); }
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      if (sidebar && sidebar.classList.contains("open")) closeSidebar(); else openSidebar();
    });
  }
  if (overlay) overlay.addEventListener("click", closeSidebar);
  if (sidebar) {
    sidebar.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeSidebar);
    });
  }

  /* ============ Active section highlight in sidebar ============ */
  const sections = document.querySelectorAll(".content-section");
  const navLinks = document.querySelectorAll("#sidebar-nav a");
  const linkByTarget = {};
  navLinks.forEach(function (a) { linkByTarget[a.dataset.target] = a; });
  if ("IntersectionObserver" in window && sections.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        const link = linkByTarget[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          navLinks.forEach(function (l) { l.classList.remove("active"); });
          link.classList.add("active");
        }
      });
    }, { rootMargin: "-10% 0px -75% 0px", threshold: 0 });
    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ============ Copy-to-clipboard on code blocks ============ */
  const COPY_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a1 1 0 01-1-1V4a1 1 0 011-1h10a1 1 0 011 1v1"/></svg>';
  const CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  document.querySelectorAll(".code-block").forEach(function (block) {
    const tab = block.querySelector(".code-tab");
    const codeEl = block.querySelector("code");
    if (!tab || !codeEl) return;
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.type = "button";
    btn.setAttribute("aria-label", "Copiar código");
    btn.innerHTML = COPY_ICON + "<span>Copiar</span>";
    btn.addEventListener("click", async function () {
      const text = codeEl.textContent;
      let ok = true;
      try {
        await navigator.clipboard.writeText(text);
      } catch (e) {
        try {
          const ta = document.createElement("textarea");
          ta.value = text;
          ta.style.position = "fixed";
          ta.style.opacity = "0";
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          document.body.removeChild(ta);
        } catch (e2) { ok = false; }
      }
      if (ok) {
        btn.classList.add("copied");
        btn.innerHTML = CHECK_ICON + "<span>Copiado</span>";
        setTimeout(function () {
          btn.classList.remove("copied");
          btn.innerHTML = COPY_ICON + "<span>Copiar</span>";
        }, 1700);
      }
    });
    tab.appendChild(btn);
  });

  /* ============ CSS selector playground ============ */
  const pgRoot = document.getElementById("pgRoot");
  const pgInput = document.getElementById("pgInput");
  const pgResult = document.getElementById("pgResult");
  const pgRunBtn = document.getElementById("pgRunBtn");

  function pgApply(sel) {
    if (!pgRoot) return;
    pgRoot.querySelectorAll(".pg-hit").forEach(function (el) { el.classList.remove("pg-hit"); });
    if (!sel || !sel.trim()) {
      pgResult.textContent = "Escribí o tocá un selector para probarlo.";
      pgResult.className = "pg-result";
      return;
    }
    let matches;
    try {
      matches = pgRoot.querySelectorAll(sel);
    } catch (e) {
      pgResult.textContent = "✕ Selector inválido: " + e.message;
      pgResult.className = "pg-result err";
      return;
    }
    matches.forEach(function (el) { el.classList.add("pg-hit"); });
    if (matches.length === 0) {
      pgResult.textContent = "0 elementos encontrados (selector válido, pero no matchea nada acá)";
      pgResult.className = "pg-result err";
    } else {
      pgResult.textContent = "✓ " + matches.length + (matches.length === 1 ? " elemento encontrado" : " elementos encontrados");
      pgResult.className = "pg-result ok";
    }
  }
  if (pgInput) {
    pgInput.addEventListener("input", function () { pgApply(pgInput.value); });
    if (pgRunBtn) pgRunBtn.addEventListener("click", function () { pgApply(pgInput.value); });
    pgInput.addEventListener("keydown", function (e) { if (e.key === "Enter") pgApply(pgInput.value); });
    document.querySelectorAll(".pg-chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        pgInput.value = chip.dataset.sel;
        pgApply(chip.dataset.sel);
        pgInput.focus();
      });
    });
  }

  /* ============ Interactive checklists (persisted) ============ */
  function updateChecklistProgress(list) {
    if (!list) return;
    const all = list.querySelectorAll('input[type="checkbox"]');
    const checked = list.querySelectorAll('input[type="checkbox"]:checked');
    const prog = list.previousElementSibling;
    if (prog && prog.classList.contains("checklist-progress")) {
      prog.textContent = checked.length + " / " + all.length + " completados";
    }
  }
  document.querySelectorAll('.check-item input[type="checkbox"]').forEach(async function (input) {
    const key = "cy-guide-checklist:" + input.dataset.key;
    const saved = await storeGet(key);
    if (saved === "true") input.checked = true;
    updateChecklistProgress(input.closest("ul.checklist"));
    input.addEventListener("change", function () {
      storeSet(key, input.checked ? "true" : "false");
      updateChecklistProgress(input.closest("ul.checklist"));
    });
  });

  /* ============ In-page search ============ */
  const searchInput = document.getElementById("searchInput");
  const searchNavEl = document.getElementById("searchNav");
  const searchCount = document.getElementById("searchCount");
  let hits = [];
  let hitIndex = -1;

  function clearHits() {
    document.querySelectorAll("mark.search-hit").forEach(function (m) {
      const parent = m.parentNode;
      if (!parent) return;
      parent.replaceChild(document.createTextNode(m.textContent), m);
      parent.normalize();
    });
    hits = [];
    hitIndex = -1;
  }

  function runSearch(query) {
    clearHits();
    if (!query || query.trim().length < 2) {
      if (searchNavEl) searchNavEl.style.display = "none";
      return;
    }
    const q = query.trim().toLowerCase();
    const main = document.querySelector("main.content");
    if (!main) return;
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        if (!node.nodeValue || node.nodeValue.toLowerCase().indexOf(q) === -1) return NodeFilter.FILTER_REJECT;
        const p = node.parentElement;
        if (!p || p.tagName === "SCRIPT" || p.tagName === "STYLE") return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    const nodes = [];
    let n;
    while ((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function (node) {
      const text = node.nodeValue;
      const lower = text.toLowerCase();
      let idx = 0, last = 0;
      const frag = document.createDocumentFragment();
      while ((idx = lower.indexOf(q, last)) !== -1) {
        if (idx > last) frag.appendChild(document.createTextNode(text.slice(last, idx)));
        const mark = document.createElement("mark");
        mark.className = "search-hit";
        mark.textContent = text.slice(idx, idx + q.length);
        frag.appendChild(mark);
        hits.push(mark);
        last = idx + q.length;
      }
      if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
      if (node.parentNode) node.parentNode.replaceChild(frag, node);
    });
    if (searchNavEl) searchNavEl.style.display = "flex";
    if (hits.length) {
      hitIndex = 0;
      focusHit();
    } else if (searchCount) {
      searchCount.textContent = "0/0";
    }
  }

  function focusHit() {
    hits.forEach(function (h) { h.classList.remove("current"); });
    if (hits[hitIndex]) {
      hits[hitIndex].classList.add("current");
      hits[hitIndex].scrollIntoView({ behavior: "smooth", block: "center" });
      if (searchCount) searchCount.textContent = (hitIndex + 1) + "/" + hits.length;
    }
  }

  let searchTimer;
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimer);
      const v = searchInput.value;
      searchTimer = setTimeout(function () { runSearch(v); }, 220);
    });
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        if (hits.length) { hitIndex = (hitIndex + 1) % hits.length; focusHit(); }
      } else if (e.key === "Escape") {
        searchInput.value = "";
        clearHits();
        if (searchNavEl) searchNavEl.style.display = "none";
        searchInput.blur();
      }
    });
  }
  const searchNextBtn = document.getElementById("searchNext");
  const searchPrevBtn = document.getElementById("searchPrev");
  if (searchNextBtn) searchNextBtn.addEventListener("click", function () { if (hits.length) { hitIndex = (hitIndex + 1) % hits.length; focusHit(); } });
  if (searchPrevBtn) searchPrevBtn.addEventListener("click", function () { if (hits.length) { hitIndex = (hitIndex - 1 + hits.length) % hits.length; focusHit(); } });

  /* keyboard shortcut: "/" focuses search */
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== searchInput && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
      e.preventDefault();
      if (searchInput) searchInput.focus();
    }
  });

  /* ============ Track switcher (Cypress / Playwright) ============ */
  var TRACK_KEY = "cy-guide-track";
  var currentTrack = "cypress";

  function applyTrack(track) {
    currentTrack = track;
    storeSet(TRACK_KEY, track);

    document.querySelectorAll(".content-section[data-track]").forEach(function(sec) {
      if (sec.dataset.track === track) { sec.classList.add("track-visible"); }
      else { sec.classList.remove("track-visible"); }
    });

    var cypressNav = document.getElementById("sidebar-nav");
    var pwNav = document.getElementById("sidebar-nav-pw");
    if (cypressNav) {
      if (track === "cypress") { cypressNav.classList.remove("track-hidden"); }
      else { cypressNav.classList.add("track-hidden"); }
    }
    if (pwNav) {
      if (track === "playwright") { pwNav.classList.add("track-visible"); }
      else { pwNav.classList.remove("track-visible"); }
    }

    document.querySelectorAll(".track-btn").forEach(function(btn) {
      if (btn.dataset.track === track) { btn.classList.add("active"); }
      else { btn.classList.remove("active"); }
    });

    rewireObserver();
  }

  function rewireObserver() {
    var visibleSections = document.querySelectorAll(".content-section.track-visible");
    var allNavLinks = document.querySelectorAll("#sidebar-nav a, #sidebar-nav-pw a");
    var linkByTarget = {};
    allNavLinks.forEach(function(a) { linkByTarget[a.dataset.target] = a; });
    if ("IntersectionObserver" in window && visibleSections.length) {
      if (window._trackObserver) window._trackObserver.disconnect();
      window._trackObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          var link = linkByTarget[entry.target.id];
          if (!link) return;
          if (entry.isIntersecting) {
            allNavLinks.forEach(function(l) { l.classList.remove("active"); });
            link.classList.add("active");
          }
        });
      }, { rootMargin: "-10% 0px -75% 0px", threshold: 0 });
      visibleSections.forEach(function(s) { window._trackObserver.observe(s); });
    }
  }

  document.querySelectorAll(".track-btn").forEach(function(btn) {
    btn.addEventListener("click", function() { applyTrack(btn.dataset.track); });
  });

  (async function() {
    var saved = await storeGet(TRACK_KEY);
    applyTrack(saved === "playwright" ? "playwright" : "cypress");
  })();

  /* ============ Playwright locator playground (simulated) ============ */
  var pwRoot = document.getElementById("pwPgRoot");
  var pwInput = document.getElementById("pwPgInput");
  var pwResult = document.getElementById("pwPgResult");
  var pwRunBtn = document.getElementById("pwPgRunBtn");

  function getImplicitRole(el) {
    var tag = el.tagName.toLowerCase();
    var type = (el.getAttribute("type") || "").toLowerCase();
    if (tag === "button" || (tag === "input" && (type === "submit" || type === "button"))) return "button";
    if (tag === "a" && el.hasAttribute("href")) return "link";
    if (/^h[1-6]$/.test(tag)) return "heading";
    if (tag === "input" && ["text","email","password","search","","tel","url"].indexOf(type) !== -1) return "textbox";
    if (tag === "input" && type === "checkbox") return "checkbox";
    if (tag === "input" && type === "radio") return "radio";
    if (tag === "select") return "combobox";
    if (tag === "textarea") return "textbox";
    if (tag === "li") return "listitem";
    return el.getAttribute("role") || "";
  }

  function getAccessibleName(el) {
    if (el.getAttribute("aria-label")) return el.getAttribute("aria-label");
    var labelledById = el.getAttribute("aria-labelledby");
    if (labelledById) { var ref = document.getElementById(labelledById); if (ref) return ref.textContent.trim(); }
    if (el.id && pwRoot) {
      var lbl = pwRoot.querySelector('label[for="' + el.id + '"]');
      if (lbl) { var c = lbl.cloneNode(true); c.querySelectorAll("input,select,textarea").forEach(function(x){x.remove();}); return c.textContent.trim(); }
    }
    var par = el.parentElement;
    if (par && par.tagName.toLowerCase() === "label") {
      var cl = par.cloneNode(true); cl.querySelectorAll("input,select,textarea").forEach(function(x){x.remove();}); return cl.textContent.trim();
    }
    return el.textContent.trim();
  }

  function pwSimulateLocator(expr) {
    if (!pwRoot) return [];
    pwRoot.querySelectorAll(".pg-hit").forEach(function(el) { el.classList.remove("pg-hit"); });
    var m;
    m = expr.match(/getByRole\s*\(\s*['"]([^'"]+)['"](?:\s*,\s*\{[^}]*name\s*:\s*['"]([^'"]*)['"][^}]*\})?/i);
    if (m) {
      var role = m[1].toLowerCase(), name = m[2] ? m[2].toLowerCase() : null;
      return Array.from(pwRoot.querySelectorAll("*")).filter(function(el) {
        var elRole = (el.getAttribute("role") || getImplicitRole(el)).toLowerCase();
        if (elRole !== role) return false;
        return !name || getAccessibleName(el).toLowerCase().indexOf(name) !== -1;
      });
    }
    m = expr.match(/getByLabel\s*\(\s*['"]([^'"]+)['"]/i);
    if (m) { var lt = m[1].toLowerCase(); return Array.from(pwRoot.querySelectorAll("input,select,textarea")).filter(function(el) { return getAccessibleName(el).toLowerCase().indexOf(lt) !== -1; }); }
    m = expr.match(/getByText\s*\(\s*['"]([^'"]+)['"]/i);
    if (m) { var tx = m[1].toLowerCase(); return Array.from(pwRoot.querySelectorAll("*")).filter(function(el) { return el.children.length===0 && el.textContent.toLowerCase().indexOf(tx)!==-1; }); }
    m = expr.match(/getByPlaceholder\s*\(\s*['"]([^'"]+)['"]/i);
    if (m) { var ph = m[1].toLowerCase(); return Array.from(pwRoot.querySelectorAll("[placeholder]")).filter(function(el){return (el.getAttribute("placeholder")||"").toLowerCase().indexOf(ph)!==-1;}); }
    m = expr.match(/getByTestId\s*\(\s*['"]([^'"]+)['"]/i);
    if (m) { return Array.from(pwRoot.querySelectorAll('[data-testid="' + m[1] + '"]')); }
    m = expr.match(/getByAltText\s*\(\s*['"]([^'"]+)['"]/i);
    if (m) { var at=m[1].toLowerCase(); return Array.from(pwRoot.querySelectorAll("[alt]")).filter(function(el){return (el.getAttribute("alt")||"").toLowerCase().indexOf(at)!==-1;}); }
    return null;
  }

  function pwRunPlayground(expr) {
    if (!pwRoot || !pwResult) return;
    pwRoot.querySelectorAll(".pg-hit").forEach(function(el) { el.classList.remove("pg-hit"); });
    if (!expr || !expr.trim()) { pwResult.textContent = "Seleccioná o escribí un locator para probarlo."; pwResult.className = "pg-result"; return; }
    var matches = pwSimulateLocator(expr);
    if (matches === null) { pwResult.textContent = "Locator no reconocido. Probá getByRole, getByLabel, getByText, getByPlaceholder o getByTestId."; pwResult.className = "pg-result err"; return; }
    matches.forEach(function(el) { el.classList.add("pg-hit"); });
    if (matches.length === 0) {
      pwResult.textContent = "0 elementos encontrados"; pwResult.className = "pg-result err";
    } else {
      pwResult.textContent = "≈ " + matches.length + (matches.length === 1 ? " elemento aproximado" : " elementos aproximados") + " (simulación educativa)";
      pwResult.className = "pg-result ok";
    }
  }

  if (pwInput) {
    pwInput.addEventListener("input", function() { pwRunPlayground(pwInput.value); });
    if (pwRunBtn) pwRunBtn.addEventListener("click", function() { pwRunPlayground(pwInput.value); });
    pwInput.addEventListener("keydown", function(e) { if (e.key === "Enter") pwRunPlayground(pwInput.value); });
    document.querySelectorAll(".pw-pg-chip").forEach(function(chip) {
      chip.addEventListener("click", function() {
        var sel = chip.dataset.pwSel || chip.textContent.trim();
        pwInput.value = sel; pwRunPlayground(sel); pwInput.focus();
      });
    });
  }

})();
"""
