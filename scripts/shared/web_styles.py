CSS = r"""
:root {
  --bg: #ffffff;
  --bg-alt: #f8fafc;
  --bg-sidebar: #f8fafc;
  --bg-elevated: #ffffff;
  --text: #1e293b;
  --text-dim: #64748b;
  --text-faint: #94a3b8;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --accent: #0d9488;
  --accent-dark: #0f766e;
  --accent-bg: #f0fdfa;
  --accent-soft: #ccfbf1;
  --navy: #0f172a;
  --navy-soft: #1e293b;
  --code-bg: #0f172a;
  --code-tab: #1e293b;
  --code-border: #334155;
  --code-text: #e2e8f0;
  --shadow: 0 1px 2px rgba(15,23,42,0.06), 0 4px 16px rgba(15,23,42,0.06);
  --shadow-lg: 0 8px 30px rgba(15,23,42,0.12);
  --radius: 10px;
  --mark-bg: #fde68a;
  --font-sans: 'Inter', 'Liberation Sans', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
  --font-mono: 'JetBrains Mono', 'DejaVu Sans Mono', 'Consolas', monospace;
}

[data-theme="dark"] {
  --bg: #0b1220;
  --bg-alt: #0f172a;
  --bg-sidebar: #0a0f1c;
  --bg-elevated: #111c30;
  --text: #e2e8f0;
  --text-dim: #94a3b8;
  --text-faint: #64748b;
  --border: #1e293b;
  --border-strong: #334155;
  --accent: #2dd4bf;
  --accent-dark: #5eead4;
  --accent-bg: #0d2c28;
  --accent-soft: #134e4a;
  --navy: #0b1220;
  --navy-soft: #0f172a;
  --code-bg: #060b15;
  --code-tab: #0f172a;
  --code-border: #1e293b;
  --code-text: #e2e8f0;
  --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 4px 20px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.45);
  --mark-bg: #92742a;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
}

body {
  margin: 0;
  font-family: var(--font-sans);
  background: var(--bg);
  color: var(--text);
  font-size: 16px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  transition: background 0.25s ease, color 0.25s ease;
}

a { color: var(--accent-dark); }
[data-theme="dark"] a { color: var(--accent); }

::selection { background: var(--accent-soft); }

/* ============== PROGRESS BAR ============== */
#progress-bar {
  position: fixed; top: 0; left: 0; height: 3px; width: 0%;
  background: linear-gradient(90deg, var(--accent), #5eead4);
  z-index: 1000; transition: width 0.1s ease-out;
}

/* ============== TOP HEADER ============== */
header.topbar {
  position: sticky; top: 0; z-index: 500;
  display: flex; align-items: center; gap: 14px;
  height: 60px; padding: 0 18px;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}
.topbar-logo {
  font-weight: 800; font-size: 17px; color: var(--text);
  display: flex; align-items: center; gap: 8px; white-space: nowrap;
}
.topbar-logo .dot { color: var(--accent); }
.topbar-logo-badge {
  width: 26px; height: 26px; border-radius: 7px;
  background: linear-gradient(135deg, var(--navy), var(--accent-dark));
  display: flex; align-items: center; justify-content: center;
  color: #5eead4; font-size: 13px; font-weight: 800;
}
.menu-toggle {
  display: none; background: none; border: 1px solid var(--border); border-radius: 8px;
  width: 38px; height: 38px; color: var(--text); cursor: pointer; align-items: center; justify-content: center;
}
.menu-toggle svg { width: 18px; height: 18px; }

.search-wrap {
  flex: 1; max-width: 420px; position: relative; margin-left: 8px;
}
.search-wrap input {
  width: 100%; padding: 8px 36px 8px 34px; border-radius: 8px;
  border: 1px solid var(--border); background: var(--bg-alt); color: var(--text);
  font-size: 13.5px; font-family: var(--font-sans);
}
.search-wrap input:focus { outline: 2px solid var(--accent); outline-offset: -1px; }
.search-icon {
  position: absolute; left: 11px; top: 50%; transform: translateY(-50%);
  color: var(--text-faint); pointer-events: none;
}
.search-icon svg { width: 15px; height: 15px; }
.search-nav {
  position: absolute; right: 4px; top: 50%; transform: translateY(-50%);
  display: none; align-items: center; gap: 2px; font-size: 11px; color: var(--text-dim);
}
.search-nav button {
  background: none; border: none; color: var(--text-dim); cursor: pointer; padding: 3px 5px; border-radius: 4px;
}
.search-nav button:hover { background: var(--border); }

.topbar-actions { margin-left: auto; display: flex; align-items: center; gap: 8px; }
.icon-btn {
  background: none; border: 1px solid var(--border); border-radius: 8px;
  width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
  color: var(--text-dim); cursor: pointer; transition: all 0.15s ease;
}
.icon-btn:hover { border-color: var(--accent); color: var(--accent); }
.icon-btn svg { width: 17px; height: 17px; }
#theme-toggle .sun { display: none; }
[data-theme="dark"] #theme-toggle .sun { display: block; }
[data-theme="dark"] #theme-toggle .moon { display: none; }

mark.search-hit {
  background: var(--mark-bg); color: inherit; border-radius: 2px; padding: 0 1px;
}
mark.search-hit.current { outline: 2px solid var(--accent); }

/* ============== LAYOUT ============== */
.layout { display: flex; max-width: 1320px; margin: 0 auto; align-items: flex-start; }

aside.sidebar {
  width: 280px; flex-shrink: 0; position: sticky; top: 60px;
  height: calc(100vh - 60px); overflow-y: auto;
  padding: 22px 14px 40px 18px; background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  scrollbar-width: thin;
}
aside.sidebar::-webkit-scrollbar { width: 6px; }
aside.sidebar::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }

.sidebar-group-label {
  font-size: 10.5px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  color: var(--text-faint); margin: 18px 8px 8px 8px;
}
.sidebar-group-label:first-child { margin-top: 4px; }

.sidebar nav a {
  display: flex; align-items: center; gap: 9px;
  padding: 7px 8px; border-radius: 7px; font-size: 13.5px; font-weight: 500;
  color: var(--text-dim); text-decoration: none; margin-bottom: 1px;
  border-left: 2px solid transparent;
}
.sidebar nav a .num {
  width: 18px; height: 18px; border-radius: 50%; background: var(--border);
  color: var(--text-dim); font-size: 9.5px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.sidebar nav a:hover { background: var(--bg-elevated); color: var(--text); }
.sidebar nav a.active { color: var(--accent-dark); background: var(--accent-bg); font-weight: 700; }
[data-theme="dark"] .sidebar nav a.active { color: var(--accent); }
.sidebar nav a.active .num { background: var(--accent); color: #fff; }

main.content { flex: 1; min-width: 0; padding: 0 0 80px 0; }

.overlay-backdrop {
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 400;
}

/* ============== HERO ============== */
.hero {
  background: radial-gradient(1200px 500px at 15% -10%, color-mix(in srgb, var(--accent) 18%, transparent), transparent),
              var(--bg-alt);
  border-bottom: 1px solid var(--border);
  padding: 56px 48px 44px 48px;
}
.hero-kicker {
  display: inline-flex; align-items: center; gap: 7px;
  font-size: 11.5px; font-weight: 700; letter-spacing: 1.6px; text-transform: uppercase;
  color: var(--accent-dark); background: var(--accent-bg); border: 1px solid var(--accent-soft);
  padding: 5px 13px; border-radius: 20px; margin-bottom: 20px;
}
[data-theme="dark"] .hero-kicker { color: var(--accent); }
.hero h1 {
  font-size: 42px; font-weight: 800; line-height: 1.1; margin: 0 0 14px 0; letter-spacing: -1px;
}
.hero h1 .accent { color: var(--accent-dark); }
[data-theme="dark"] .hero h1 .accent { color: var(--accent); }
.hero p.lead { font-size: 17px; color: var(--text-dim); max-width: 640px; margin: 0 0 24px 0; }
.hero-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.hero-pill {
  background: var(--bg-elevated); border: 1px solid var(--border); color: var(--text-dim);
  font-size: 12.5px; padding: 6px 13px; border-radius: 20px; font-weight: 500;
}

/* ============== SECTIONS ============== */
.content-section { padding: 46px 48px 8px 48px; scroll-margin-top: 70px; }
.content-section:last-of-type { padding-bottom: 60px; }
.section-eyebrow {
  color: var(--accent-dark); font-weight: 700; font-size: 12px; letter-spacing: 1.6px;
  text-transform: uppercase; margin-bottom: 8px;
}
[data-theme="dark"] .section-eyebrow { color: var(--accent); }
h1.section-title {
  font-size: 30px; font-weight: 800; color: var(--text); margin: 0 0 26px 0;
  padding-bottom: 16px; border-bottom: 2px solid var(--border);
  display: flex; align-items: center; gap: 10px; scroll-margin-top: 70px;
}
.section-title .num-chip {
  background: var(--accent); color: #fff; width: 34px; height: 34px; border-radius: 9px;
  display: inline-flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0;
}
h2 {
  font-size: 19px; font-weight: 700; color: var(--text); margin: 36px 0 14px 0;
  padding-left: 12px; border-left: 4px solid var(--accent); scroll-margin-top: 70px;
}
h3 { font-size: 15.5px; font-weight: 700; color: var(--accent-dark); margin: 22px 0 10px 0; }
[data-theme="dark"] h3 { color: var(--accent); }
p { margin: 0 0 13px 0; color: var(--text); }
ul, ol { margin: 0 0 14px 0; padding-left: 22px; }
li { margin-bottom: 6px; }
strong { color: var(--text); font-weight: 700; }
code.inline {
  font-family: var(--font-mono); background: var(--bg-alt); color: var(--accent-dark);
  border: 1px solid var(--border); padding: 1.5px 6px; border-radius: 4px; font-size: 0.87em;
}
[data-theme="dark"] code.inline { color: var(--accent); }

/* ============== CODE BLOCKS ============== */
.code-block {
  background: var(--code-bg); border: 1px solid var(--code-border); border-radius: 10px;
  overflow: hidden; margin: 16px 0 20px 0; box-shadow: var(--shadow); position: relative;
}
.code-tab {
  background: var(--code-tab); padding: 9px 12px; display: flex; align-items: center; gap: 6px;
  border-bottom: 1px solid var(--code-border);
}
.code-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.d1 { background: #f87171; } .d2 { background: #fbbf24; } .d3 { background: #4ade80; }
.code-filename { margin-left: 7px; color: #94a3b8; font-size: 12px; font-family: var(--font-mono); }
.copy-btn {
  margin-left: auto; background: rgba(255,255,255,0.06); border: 1px solid var(--code-border);
  color: #cbd5e1; font-size: 11.5px; padding: 4px 10px; border-radius: 6px; cursor: pointer;
  display: flex; align-items: center; gap: 5px; font-family: var(--font-sans); transition: all 0.15s ease;
}
.copy-btn:hover { background: rgba(255,255,255,0.14); color: #fff; }
.copy-btn svg { width: 12.5px; height: 12.5px; }
.copy-btn.copied { background: var(--accent); border-color: var(--accent); color: #06281f; }
.code-block pre { margin: 0; padding: 16px 18px; overflow-x: auto; }
.code-block code {
  font-family: var(--font-mono); font-size: 13.3px; line-height: 1.6; color: var(--code-text);
  white-space: pre;
}
.tok-k  { color: #93c5fd; font-weight: bold; }
.tok-s  { color: #86efac; }
.tok-c  { color: #64748b; font-style: italic; }
.tok-n  { color: #fcd34d; }
.tok-cy { color: #5eead4; font-weight: bold; }

/* ============== CALLOUTS ============== */
.callout {
  border-radius: 10px; padding: 16px 18px; margin: 16px 0 20px 0; border-left: 4px solid;
}
.callout-head { font-weight: 700; font-size: 14.5px; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.callout-badge {
  font-size: 10px; font-weight: 700; letter-spacing: 0.6px; padding: 2px 8px; border-radius: 5px; color: #fff;
}
.callout-body { font-size: 14.5px; color: var(--text-dim); }
.callout-body p:last-child { margin-bottom: 0; }
.callout-body code.inline { font-size: 0.85em; }

.callout-tip      { background: var(--accent-bg); border-color: #2563eb; background: color-mix(in srgb, #2563eb 7%, var(--bg-elevated)); }
.callout-tip .callout-badge      { background: #2563eb; }
.callout-tip .callout-head       { color: #2563eb; }

.callout-warning  { border-color: #d97706; background: color-mix(in srgb, #d97706 9%, var(--bg-elevated)); }
.callout-warning .callout-badge  { background: #d97706; }
.callout-warning .callout-head   { color: #d97706; }

.callout-best     { border-color: #16a34a; background: color-mix(in srgb, #16a34a 8%, var(--bg-elevated)); }
.callout-best .callout-badge     { background: #16a34a; }
.callout-best .callout-head      { color: #16a34a; }

.callout-bad      { border-color: #dc2626; background: color-mix(in srgb, #dc2626 7%, var(--bg-elevated)); }
.callout-bad .callout-badge      { background: #dc2626; }
.callout-bad .callout-head       { color: #dc2626; }

.callout-info     { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 9%, var(--bg-elevated)); }
.callout-info .callout-badge     { background: var(--accent); }
.callout-info .callout-head      { color: var(--accent-dark); }

.callout-note     { border-color: var(--text-faint); background: var(--bg-alt); }
.callout-note .callout-badge     { background: var(--text-faint); }
.callout-note .callout-head      { color: var(--text-dim); }

/* ============== TABLES ============== */
.table-scroll { overflow-x: auto; margin: 16px 0 22px 0; border-radius: 10px; border: 1px solid var(--border); }
table.ref-table { width: 100%; border-collapse: collapse; font-size: 13.6px; }
table.ref-table thead tr { background: var(--navy); }
table.ref-table th { color: #fff; text-align: left; padding: 11px 14px; font-weight: 700; font-size: 12px; }
table.ref-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); vertical-align: top; color: var(--text); }
table.ref-table tbody tr:hover { background: var(--bg-alt); }
table.ref-table code.inline { white-space: nowrap; }

/* ============== DIAGRAMS ============== */
figure.diagram { margin: 18px 0 24px 0; text-align: center; }
.diagram-svg {
  display: flex; justify-content: center; background: var(--bg-elevated);
  border: 1px solid var(--border); border-radius: 10px; padding: 14px; overflow-x: auto;
}
.diagram-svg svg { max-width: 100%; height: auto; }
figure.diagram figcaption { font-size: 12.5px; color: var(--text-faint); margin-top: 8px; font-style: italic; }

/* ============== MISC ============== */
.two-col { display: flex; gap: 16px; margin: 16px 0 20px 0; flex-wrap: wrap; }
.two-col > div { flex: 1; min-width: 260px; }

.kpi-row { display: flex; gap: 12px; margin: 18px 0 22px 0; flex-wrap: wrap; }
.kpi {
  flex: 1; min-width: 150px; background: var(--accent-bg); border: 1px solid var(--accent-soft);
  border-radius: 10px; padding: 16px; text-align: center;
}
.kpi .kpi-num { font-size: 24px; font-weight: 800; color: var(--accent-dark); display: block; margin-bottom: 4px; }
[data-theme="dark"] .kpi .kpi-num { color: var(--accent); }
.kpi .kpi-label { font-size: 12px; color: var(--text-dim); }

.steps { list-style: none; padding: 0; margin: 18px 0 20px 0; counter-reset: step; }
.steps > li { counter-increment: step; position: relative; padding-left: 38px; margin-bottom: 22px; }
.steps > li::before {
  content: counter(step); position: absolute; left: 0; top: 1px;
  background: var(--accent); color: #fff; font-weight: 700; font-size: 12.5px;
  width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
}
.step-title { font-weight: 700; color: var(--text); margin-bottom: 4px; font-size: 15.5px; }

.badge-row { display: flex; gap: 8px; flex-wrap: wrap; margin: 12px 0 18px 0; }
.tag {
  background: var(--bg-alt); border: 1px solid var(--border); color: var(--text-dim);
  font-size: 12.5px; padding: 5px 11px; border-radius: 6px; font-family: var(--font-mono);
}

.end-box {
  background: linear-gradient(160deg, var(--navy), var(--accent-dark));
  color: #fff; border-radius: 14px; padding: 32px; text-align: center; margin: 32px 0 12px 0;
}
.end-box h3 { color: #5eead4; margin-top: 0; font-size: 20px; }
.end-box p { color: #cbd5e1; max-width: 560px; margin: 0 auto; }
.end-box code.inline { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.2); color: #5eead4; }

/* ============== INTERACTIVE CHECKLIST ============== */
ul.checklist { list-style: none; padding: 0; margin: 16px 0 20px 0; }
ul.checklist li { margin-bottom: 0; }
.check-item {
  display: flex; align-items: flex-start; gap: 11px; padding: 9px 12px; border-radius: 9px;
  cursor: pointer; transition: background 0.15s ease; border: 1px solid transparent;
}
.check-item:hover { background: var(--bg-alt); border-color: var(--border); }
.check-item input { display: none; }
.check-box {
  width: 20px; height: 20px; border-radius: 6px; border: 2px solid var(--border-strong);
  flex-shrink: 0; margin-top: 1px; display: flex; align-items: center; justify-content: center;
  transition: all 0.15s ease;
}
.check-box svg { width: 12px; height: 12px; opacity: 0; transform: scale(0.5); transition: all 0.15s ease; stroke: #fff; }
.check-item input:checked + .check-box { background: var(--accent); border-color: var(--accent); }
.check-item input:checked + .check-box svg { opacity: 1; transform: scale(1); }
.check-text { font-size: 14.3px; color: var(--text); }
.check-item input:checked ~ .check-text { color: var(--text-faint); text-decoration: line-through; }
.checklist-progress {
  font-size: 12px; color: var(--text-faint); margin-bottom: 6px; font-weight: 600;
}

/* ============== DETAILS / PRACTICE REVEAL ============== */
details.reveal {
  border: 1px solid var(--border); border-radius: 9px; margin-bottom: 10px;
  background: var(--bg-elevated); overflow: hidden;
}
details.reveal summary {
  padding: 13px 16px; cursor: pointer; font-weight: 600; font-size: 14px;
  list-style: none; display: flex; align-items: center; gap: 10px; color: var(--text);
}
details.reveal summary::-webkit-details-marker { display: none; }
details.reveal summary .chev { transition: transform 0.2s ease; color: var(--text-faint); flex-shrink: 0; }
details.reveal summary .chev svg { width: 16px; height: 16px; }
details.reveal[open] summary .chev { transform: rotate(90deg); }
details.reveal summary code.inline { font-size: 13px; }
details.reveal .reveal-body {
  padding: 0 16px 15px 42px; font-size: 13.8px; color: var(--text-dim); border-top: 1px solid var(--border);
  padding-top: 12px;
}

/* ============== CSS SELECTOR PLAYGROUND ============== */
.playground {
  border: 1px solid var(--border); border-radius: 14px; overflow: hidden; margin: 22px 0 28px 0;
  background: var(--bg-elevated); box-shadow: var(--shadow);
}
.playground-head {
  padding: 16px 20px; border-bottom: 1px solid var(--border);
  background: var(--bg-alt);
}
.playground-head h3 { margin: 0 0 4px 0; font-size: 16px; color: var(--text); }
.playground-head p { margin: 0; font-size: 13px; color: var(--text-dim); }
.playground-body { display: flex; flex-wrap: wrap; }
.playground-controls { flex: 1; min-width: 280px; padding: 18px 20px; border-right: 1px solid var(--border); }
.playground-preview { flex: 1; min-width: 280px; padding: 18px 20px; background: var(--bg-alt); }

.pg-input-row { display: flex; gap: 8px; margin-bottom: 10px; }
.pg-input-row input {
  flex: 1; font-family: var(--font-mono); font-size: 13.5px; padding: 9px 12px;
  border-radius: 8px; border: 1px solid var(--border-strong); background: var(--bg); color: var(--text);
}
.pg-input-row input:focus { outline: 2px solid var(--accent); outline-offset: -1px; }
.pg-input-row button {
  background: var(--accent); border: none; color: #fff; font-weight: 600; font-size: 13px;
  padding: 0 16px; border-radius: 8px; cursor: pointer; white-space: nowrap;
}
.pg-input-row button:hover { background: var(--accent-dark); }
.pg-result { font-size: 12.5px; font-weight: 600; margin-bottom: 14px; min-height: 18px; font-family: var(--font-mono); }
.pg-result.ok { color: var(--accent-dark); }
[data-theme="dark"] .pg-result.ok { color: var(--accent); }
.pg-result.err { color: #dc2626; }
.pg-chip-label { font-size: 11.5px; font-weight: 700; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.6px; margin: 14px 0 8px 0; }
.pg-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.pg-chip {
  font-family: var(--font-mono); font-size: 12px; background: var(--bg-alt); border: 1px solid var(--border);
  color: var(--text-dim); padding: 5px 10px; border-radius: 6px; cursor: pointer; transition: all 0.15s ease;
}
.pg-chip:hover { border-color: var(--accent); color: var(--accent-dark); }
[data-theme="dark"] .pg-chip:hover { color: var(--accent); }

.pg-preview-root {
  background: var(--bg); border: 1px dashed var(--border-strong); border-radius: 10px; padding: 16px;
  font-size: 13px;
}
.pg-nav { display: flex; gap: 14px; padding-bottom: 10px; margin-bottom: 12px; border-bottom: 1px solid var(--border); }
.pg-link { color: var(--text-dim); text-decoration: none; font-size: 13px; padding: 2px 4px; border-radius: 4px; }
.pg-link.pg-active { color: var(--accent-dark); font-weight: 700; }
[data-theme="dark"] .pg-link.pg-active { color: var(--accent); }
.pg-card {
  border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 10px;
  display: flex; align-items: center; justify-content: space-between; gap: 10px; background: var(--bg-elevated);
}
.pg-card h4 { margin: 0 0 2px 0; font-size: 13.5px; color: var(--text); }
.pg-price { color: var(--accent-dark); font-weight: 700; font-size: 13px; }
[data-theme="dark"] .pg-price { color: var(--accent); }
.pg-btn {
  background: var(--accent); color: #fff; border: none; border-radius: 6px; padding: 6px 12px;
  font-size: 12px; font-weight: 600; cursor: default;
}
.pg-btn:disabled { background: var(--border-strong); color: var(--text-faint); }
.pg-form { border-top: 1px solid var(--border); padding-top: 12px; margin-top: 4px; }
.pg-form label { display: block; font-size: 12px; color: var(--text-dim); margin-bottom: 4px; }
.pg-form input[type="email"] {
  width: 100%; padding: 7px 9px; border-radius: 6px; border: 1px solid var(--border-strong);
  background: var(--bg); color: var(--text); font-size: 12.5px; margin-bottom: 10px;
}
.pg-check-label { display: flex; align-items: center; gap: 6px; font-size: 12.5px; color: var(--text-dim); margin-bottom: 10px; }
.pg-list { list-style: none; padding: 0; margin: 10px 0 0 0; display: flex; gap: 8px; flex-wrap: wrap; }
.pg-list li {
  border: 1px solid var(--border); border-radius: 6px; padding: 5px 11px; font-size: 12.5px;
  color: var(--text-dim); margin: 0;
}

.pg-hit {
  outline: 2.5px solid #f59e0b !important; outline-offset: 2px; border-radius: 6px;
  background: color-mix(in srgb, #f59e0b 15%, transparent) !important;
  animation: pg-pulse 0.5s ease;
  position: relative;
}
@keyframes pg-pulse { 0% { outline-color: #f59e0b00; } 60% { outline-color: #f59e0bcc; } 100% { outline-color: #f59e0b; } }

/* ============== BACK TO TOP ============== */
#back-to-top {
  position: fixed; bottom: 26px; right: 26px; width: 44px; height: 44px; border-radius: 50%;
  background: var(--navy); color: #5eead4; border: none; cursor: pointer; display: flex;
  align-items: center; justify-content: center; box-shadow: var(--shadow-lg); z-index: 300;
  opacity: 0; pointer-events: none; transform: translateY(10px); transition: all 0.25s ease;
}
#back-to-top.show { opacity: 1; pointer-events: auto; transform: translateY(0); }
#back-to-top svg { width: 18px; height: 18px; }

/* ============== RESPONSIVE ============== */
@media (max-width: 980px) {
  .menu-toggle { display: flex; }
  aside.sidebar {
    position: fixed; top: 60px; left: 0; height: calc(100vh - 60px); z-index: 450;
    width: 280px; transform: translateX(-100%); transition: transform 0.25s ease; box-shadow: var(--shadow-lg);
  }
  aside.sidebar.open { transform: translateX(0); }
  .overlay-backdrop.show { display: block; }
  .search-wrap { display: none; }
  .hero, .content-section { padding-left: 22px; padding-right: 22px; }
  .hero h1 { font-size: 32px; }
  .playground-controls { border-right: none; border-bottom: 1px solid var(--border); }
}
@media (max-width: 600px) {
  table.ref-table { font-size: 12.5px; }
  .topbar-logo span.full { display: none; }
}

:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

/* ============== TRACK SWITCHER ============== */
.track-switcher {
  display: flex; gap: 4px; padding: 4px; background: var(--bg-alt);
  border: 1px solid var(--border); border-radius: 12px; margin: 14px 10px 6px 10px;
}
.track-btn {
  flex: 1; padding: 8px 10px; border: none; border-radius: 9px; cursor: pointer;
  font-size: 13px; font-weight: 600; color: var(--text-dim); background: transparent;
  transition: all 0.2s ease; line-height: 1.3; text-align: center;
}
.track-btn:hover { background: var(--bg-elevated); color: var(--text); }
.track-btn.active {
  background: var(--bg-elevated); color: var(--text); box-shadow: var(--shadow);
}
.track-btn.active[data-track="cypress"] { color: var(--accent-dark); border: 1px solid var(--accent-soft); }
.track-btn.active[data-track="playwright"] { color: #7c3aed; border: 1px solid #ede9fe; }
[data-theme="dark"] .track-btn.active[data-track="cypress"] { color: var(--accent); border-color: var(--accent-soft); }
[data-theme="dark"] .track-btn.active[data-track="playwright"] { color: #a78bfa; border-color: #3b2a6e; }
.track-label-badge {
  display: inline-block; font-size: 9px; font-weight: 800; letter-spacing: 0.4px;
  padding: 1px 5px; border-radius: 4px; margin-bottom: 1px;
}
.track-btn[data-track="cypress"] .track-label-badge { background: var(--accent-soft); color: var(--accent-dark); }
.track-btn[data-track="playwright"] .track-label-badge { background: #ede9fe; color: #5b21b6; }
[data-theme="dark"] .track-btn[data-track="cypress"] .track-label-badge { background: var(--accent-soft); color: var(--accent); }
[data-theme="dark"] .track-btn[data-track="playwright"] .track-label-badge { background: #3b2a6e; color: #a78bfa; }

/* Secciones mostradas/ocultas por track */
.content-section[data-track] { display: none; }
.content-section[data-track].track-visible { display: block; }

/* Sidebar navs por track */
#sidebar-nav-pw { display: none; }
#sidebar-nav-pw.track-visible { display: block; }
#sidebar-nav.track-hidden { display: none; }

/* Num-chip color para Playwright (morado en vez de teal) */
.pw-chip {
  background: #7c3aed !important;
}
[data-theme="dark"] .pw-chip { background: #6d28d9 !important; }

/* Playwright playground — nota de advertencia ya viene como callout */
.pw-playground .playground-head { background: var(--bg-alt); }
"""
