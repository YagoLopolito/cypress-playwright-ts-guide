# -*- coding: utf-8 -*-
"""
Helpers para generar el documento HTML -> PDF.
Incluye: resaltador de sintaxis simple (regex tokenizer), y builders de
componentes (code_block, callout, table, diagram wrappers).
"""
import re
import html as htmllib

# ---------------------------------------------------------------------------
# SYNTAX HIGHLIGHTER
# ---------------------------------------------------------------------------

TS_KEYWORDS = set("""
const let var function return import from export default interface type
class extends implements public private protected static async await new
if else for while of in typeof void null undefined true false this throw
try catch finally instanceof as readonly namespace declare enum break
continue switch case do delete yield get set abstract
""".split())

CY_IDENTIFIERS = set("""
cy describe it before beforeEach after afterEach context expect Cypress
""".split())

TOKEN_RE = re.compile(r"""
    (?P<comment>//[^\n]*|/\*.*?\*/)
  | (?P<string>`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<number>\b\d+\.?\d*\b)
  | (?P<word>[A-Za-z_$][A-Za-z0-9_$]*)
  | (?P<op>[{}()\[\];:,.<>=+\-*/!&|?]+)
""", re.VERBOSE | re.DOTALL)


def highlight_code(code: str, lang: str = "ts") -> str:
    """Tokeniza y resalta código TS/JS. Para bash/json/css usa reglas simplificadas."""
    if lang in ("bash", "shell", "sh"):
        return _highlight_bash(code)
    if lang == "json":
        return _highlight_json(code)
    if lang == "css":
        return _highlight_css(code)

    out = []
    pos = 0
    for m in TOKEN_RE.finditer(code):
        if m.start() > pos:
            out.append(htmllib.escape(code[pos:m.start()]))
        kind = m.lastgroup
        text = m.group()
        esc = htmllib.escape(text)
        if kind == "comment":
            out.append(f'<span class="tok-c">{esc}</span>')
        elif kind == "string":
            out.append(f'<span class="tok-s">{esc}</span>')
        elif kind == "number":
            out.append(f'<span class="tok-n">{esc}</span>')
        elif kind == "word":
            if text in TS_KEYWORDS:
                out.append(f'<span class="tok-k">{esc}</span>')
            elif text in CY_IDENTIFIERS:
                out.append(f'<span class="tok-cy">{esc}</span>')
            else:
                out.append(esc)
        else:
            out.append(esc)
        pos = m.end()
    out.append(htmllib.escape(code[pos:]))
    return "".join(out)


BASH_TOKEN_RE = re.compile(r"""
    (?P<comment>\#[^\n]*)
  | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<flag>\s--?[A-Za-z][A-Za-z0-9-]*)
  | (?P<word>[A-Za-z_][A-Za-z0-9_.-]*)
""", re.VERBOSE | re.DOTALL)

BASH_CMDS = set("npm npx node mkdir cd code echo cat git yarn pnpm tsc touch rm cp mv ls export source sudo apt brew".split())


def _highlight_bash(code: str) -> str:
    out, pos = [], 0
    for m in BASH_TOKEN_RE.finditer(code):
        if m.start() > pos:
            out.append(htmllib.escape(code[pos:m.start()]))
        kind = m.lastgroup
        text = m.group()
        esc = htmllib.escape(text)
        if kind == "comment":
            out.append(f'<span class="tok-c">{esc}</span>')
        elif kind == "string":
            out.append(f'<span class="tok-s">{esc}</span>')
        elif kind == "flag":
            out.append(f'<span class="tok-n">{esc}</span>')
        elif kind == "word" and text in BASH_CMDS:
            out.append(f'<span class="tok-k">{esc}</span>')
        else:
            out.append(esc)
        pos = m.end()
    out.append(htmllib.escape(code[pos:]))
    return "".join(out)


JSON_TOKEN_RE = re.compile(r'(?P<key>"(?:\\.|[^"\\])*"(?=\s*:))|(?P<string>"(?:\\.|[^"\\])*")|(?P<number>\b-?\d+\.?\d*\b)|(?P<bool>\btrue\b|\bfalse\b|\bnull\b)')


def _highlight_json(code: str) -> str:
    out, pos = [], 0
    for m in JSON_TOKEN_RE.finditer(code):
        if m.start() > pos:
            out.append(htmllib.escape(code[pos:m.start()]))
        kind = m.lastgroup
        esc = htmllib.escape(m.group())
        if kind == "key":
            out.append(f'<span class="tok-cy">{esc}</span>')
        elif kind == "string":
            out.append(f'<span class="tok-s">{esc}</span>')
        elif kind in ("number", "bool"):
            out.append(f'<span class="tok-n">{esc}</span>')
        pos = m.end()
    out.append(htmllib.escape(code[pos:]))
    return "".join(out)


CSS_TOKEN_RE = re.compile(r"""
    (?P<comment>/\*.*?\*/)
  | (?P<selector>^[ \t]*[.#]?[A-Za-z0-9_\-\[\]="'.,: >~+*]+(?=\s*\{))
  | (?P<prop>[A-Za-z-]+(?=\s*:))
  | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<number>\b-?\d+\.?\d*(px|em|rem|%|s|ms)?\b)
""", re.VERBOSE | re.DOTALL | re.MULTILINE)


def _highlight_css(code: str) -> str:
    out, pos = [], 0
    for m in CSS_TOKEN_RE.finditer(code):
        if m.start() > pos:
            out.append(htmllib.escape(code[pos:m.start()]))
        kind = m.lastgroup
        esc = htmllib.escape(m.group())
        if kind == "comment":
            out.append(f'<span class="tok-c">{esc}</span>')
        elif kind == "selector":
            out.append(f'<span class="tok-cy">{esc}</span>')
        elif kind == "prop":
            out.append(f'<span class="tok-k">{esc}</span>')
        elif kind == "string":
            out.append(f'<span class="tok-s">{esc}</span>')
        elif kind == "number":
            out.append(f'<span class="tok-n">{esc}</span>')
        else:
            out.append(esc)
        pos = m.end()
    out.append(htmllib.escape(code[pos:]))
    return "".join(out)


# ---------------------------------------------------------------------------
# COMPONENT BUILDERS
# ---------------------------------------------------------------------------

def code_block(code: str, lang: str = "ts", filename: str = None) -> str:
    code = code.strip("\n")
    body = highlight_code(code, lang)
    tab = f'<div class="code-tab"><span class="code-dot d1"></span><span class="code-dot d2"></span><span class="code-dot d3"></span><span class="code-filename">{htmllib.escape(filename) if filename else lang.upper()}</span></div>'
    return f'<div class="code-block">{tab}<pre><code>{body}</code></pre></div>'


CALLOUT_META = {
    "tip":      ("TIP", "callout-tip"),
    "warning":  ("ATENCIÓN", "callout-warning"),
    "best":     ("BUENA PRÁCTICA", "callout-best"),
    "bad":      ("ERROR COMÚN", "callout-bad"),
    "info":     ("INFO", "callout-info"),
    "note":     ("NOTA", "callout-note"),
}


def callout(kind: str, title: str, body_html: str) -> str:
    label, cls = CALLOUT_META[kind]
    return f'''<div class="callout {cls}">
        <div class="callout-head"><span class="callout-badge">{label}</span> {htmllib.escape(title)}</div>
        <div class="callout-body">{body_html}</div>
    </div>'''


def table(headers, rows, widths=None) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = ""
    for r in rows:
        tds = "".join(f"<td>{c}</td>" for c in r)
        trs += f"<tr>{tds}</tr>"
    style = ""
    if widths:
        cols = "".join(f'<col style="width:{w}">' for w in widths)
        style = f"<colgroup>{cols}</colgroup>"
    return f'<table class="ref-table">{style}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def figure(svg: str, caption: str) -> str:
    return f'<figure class="diagram"><div class="diagram-svg">{svg}</div><figcaption>{htmllib.escape(caption)}</figcaption></figure>'


def practice_reveal(items) -> str:
    """items: lista de tuplas (selector_html, respuesta_html). Genera <details> clickeables."""
    chev = '<span class="chev"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></span>'
    out = []
    for selector_html, answer_html in items:
        out.append(
            f'<details class="reveal"><summary>{chev}{selector_html}</summary>'
            f'<div class="reveal-body">{answer_html}</div></details>'
        )
    return "".join(out)
