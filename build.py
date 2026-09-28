#!/usr/bin/env python3
"""Regenerate the /lake-cumberland/privacy/ and /lake-cumberland/terms/ pages
from the Lake Cumberland app's own Markdown, so the app repo stays the single
source of truth (valleyside-app-personal/lake-cumberland/docs).

Usage:
    python build.py

Standard library only, no third-party dependencies.
"""

import html
import re
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = SITE_ROOT.parent / "valleyside-app-personal" / "lake-cumberland" / "docs"

PAGES = [
    {
        "markdown": SOURCE_DIR / "privacy-policy.md",
        "output": SITE_ROOT / "lake-cumberland" / "privacy" / "index.html",
        "path": "/lake-cumberland/privacy/",
        "title": "Privacy Policy — Lake Cumberland",
        "description": "Privacy policy for the Lake Cumberland app, published by Valleyside Electronics LLC.",
    },
    {
        "markdown": SOURCE_DIR / "terms.md",
        "output": SITE_ROOT / "lake-cumberland" / "terms" / "index.html",
        "path": "/lake-cumberland/terms/",
        "title": "Terms of Use — Lake Cumberland",
        "description": "Terms of use for the Lake Cumberland app, published by Valleyside Electronics LLC.",
    },
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://valleyside.dev{path}">
<meta name="theme-color" content="#0E4C5B" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A3A46" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Valleyside Electronics LLC">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="https://valleyside.dev{path}">
<meta property="og:image" content="https://valleyside.dev/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Valleyside Electronics LLC: custom software, websites and apps. Russell Springs, Kentucky.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="https://valleyside.dev/og-image.png">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/InterVariable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/">
      <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="8" fill="#F4FBFC"/><path d="M9.05 12.5q3.475-2.8 6.95 0t6.95 0L16 25.4z" fill="#56A7B8"/><path d="M6.2 7.2 16 25.4l9.8-18.2" fill="none" stroke="#0E4C5B" stroke-width="3.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <span>Valleyside</span>
    </a>
    <nav class="nav-desktop" aria-label="Main">
      <a href="/#services">Services</a>
      <a href="/#work">Work</a>
      <a href="/#products">Products</a>
      <a href="/#contact">Contact</a>
      <a href="/support/">Support</a>
      <a class="btn btn-light btn-sm" href="mailto:austin@valleyside.dev?subject=New%20project">Start a project</a>
    </nav>
    <details class="nav-mobile">
      <summary><svg class="icon icon-open" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="icon icon-close" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18"/></svg><span>Menu</span></summary>
      <nav class="nav-mobile-panel" aria-label="Main">
        <a href="/#services">Services</a>
        <a href="/#work">Work</a>
        <a href="/#products">Products</a>
        <a href="/#contact">Contact</a>
        <a href="/support/">Support</a>
        <a class="btn btn-light" href="mailto:austin@valleyside.dev?subject=New%20project">Start a project</a>
      </nav>
    </details>
  </div>
</header>

<main id="main">
<section class="band-dark page-hero" aria-labelledby="page-title">
  <svg class="contours" viewBox="0 0 1440 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
    <path d="M-40 60 C520 60 915 92 1014 228 S1110 274 1170 207 S1500 60 1480 60" opacity="0.10"/>
    <path d="M-40 116 C482 96 894 135 1006 261 S1114 304 1181 242 S1538 96 1480 112" opacity="0.12"/>
    <path d="M-40 157 C444 147 873 179 997 294 S1118 334 1193 277 S1576 147 1480 155" opacity="0.14"/>
    <path d="M-40 191 C406 205 852 222 989 328 S1121 363 1204 311 S1614 205 1480 194" opacity="0.18"/>
    <path d="M-40 235 C368 253 831 266 981 361 S1125 393 1216 346 S1652 253 1480 239" opacity="0.10"/>
    <path d="M-40 292 C330 288 810 310 972 394 S1129 423 1227 381 S1690 288 1480 291" opacity="0.12"/>
    <path d="M-40 346 C292 326 790 353 964 427 S1133 452 1238 416 S1728 326 1480 342" opacity="0.14"/>
    <path d="M-40 385 C254 379 769 397 955 460 S1137 482 1250 451 S1766 379 1480 384" opacity="0.18"/>
    <path d="M-40 420 C216 436 748 440 947 494 S1140 512 1261 485 S1804 436 1480 423" opacity="0.10"/>
    <path d="M-40 466 C178 482 727 484 939 527 S1144 541 1273 520 S1842 482 1480 469" opacity="0.12"/>
    <path d="M-40 524 C140 516 706 528 930 560 S1148 571 1284 555 S1880 516 1480 523" opacity="0.14"/>
  </svg>
  <div class="container container-text">
    <span class="eyebrow">Lake Cumberland app</span>
    <h1 id="page-title">{heading}</h1>
    {effective}
  </div>
  <svg class="wave-edge" viewBox="0 0 1440 64" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path fill="currentColor" d="M0 38C240 6 470 6 720 30s490 36 720 2V64H0z"/></svg>
</section>

<div class="page-main">
  <div class="container container-text">
    <article class="prose">
{body}
    </article>

    <h2 class="subhead">Related</h2>
    <ul class="link-list">
      <li><a href="/lake-cumberland/privacy/">Privacy policy <svg class="icon arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></li>
      <li><a href="/lake-cumberland/terms/">Terms of use <svg class="icon arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></li>
      <li><a href="/lake-cumberland/">About the Lake Cumberland app <svg class="icon arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></li>
      <li><a href="/support/">Support <svg class="icon arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></li>
    </ul>
  </div>
</div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="/">
          <svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect width="32" height="32" rx="8" fill="#0E4C5B"/><path d="M9.05 12.5q3.475-2.8 6.95 0t6.95 0L16 25.4z" fill="#9ED8E3"/><path d="M6.2 7.2 16 25.4l9.8-18.2" fill="none" stroke="#FFFFFF" stroke-width="3.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span>Valleyside</span>
        </a>
        <p>Custom software, websites and apps from Russell Springs, Kentucky, for southern Kentucky and clients anywhere.</p>
      </div>
      <div class="footer-col">
        <h2>Company</h2>
        <ul>
          <li><a href="/#services">Services</a></li>
          <li><a href="/#work">Work</a></li>
          <li><a href="/#products">Products</a></li>
          <li><a href="/lake-cumberland/">Lake Cumberland app</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Contact</h2>
        <ul>
          <li><a href="mailto:austin@valleyside.dev">austin@valleyside.dev</a></li>
          <li><a href="mailto:support@valleyside.dev">support@valleyside.dev</a></li>
          <li><a href="tel:+12704385116">270-438-5116</a></li>
          <li><a href="/support/">Support</a></li>
          <li><a href="/privacy/">Privacy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Valleyside Electronics LLC</p>
      <p>Veteran-owned &middot; Russell Springs, Kentucky</p>
    </div>
  </div>
</footer>
<script>document.querySelectorAll('.nav-mobile a').forEach(function(a){{a.addEventListener('click',function(){{a.closest('details').removeAttribute('open');}});}});</script>
</body>
</html>
"""

MAILTO_EMAIL = "support@valleyside.dev"

# Matches a Markdown link: [text](url)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)([^*]+)\*(?!\*)")


def escape(text: str) -> str:
    return html.escape(text, quote=False)


def inline_format(text: str) -> str:
    """Escape HTML, then apply Markdown links, bold, italic and the
    support@valleyside.dev mailto autolink, on already-escaped text."""

    # Escape first so raw source text (including & in URLs) is safe, but we
    # need to run link/bold/italic parsing on the *original* text so the
    # regexes see the real markdown punctuation. We escape pieces as we
    # rebuild them instead.

    out = []
    pos = 0
    # Handle links first (across the whole string), escaping the surrounding
    # plain text and the link text/url pieces, then run bold/italic over the
    # plain (non-link) spans.

    def _bold_and_italic(segment: str) -> str:
        tokens = []
        i = 0
        n = len(segment)
        while i < n:
            if segment[i:i+2] == "**":
                end = segment.find("**", i + 2)
                if end != -1:
                    tokens.append(("b", segment[i+2:end]))
                    i = end + 2
                    continue
            if segment[i] == "*":
                end = segment.find("*", i + 1)
                if end != -1:
                    tokens.append(("i", segment[i+1:end]))
                    i = end + 1
                    continue
            # plain char run
            j = i
            while j < n and segment[j] != "*":
                j += 1
            tokens.append(("t", segment[i:j]))
            i = j
        pieces = []
        for kind, val in tokens:
            if kind == "b":
                pieces.append("<strong>" + escape(val) + "</strong>")
            elif kind == "i":
                pieces.append("<em>" + escape(val) + "</em>")
            else:
                pieces.append(autolink_email(escape(val)))
        return "".join(pieces)

    def autolink_email(escaped_text: str) -> str:
        return escaped_text.replace(
            MAILTO_EMAIL,
            '<a href="mailto:{0}">{0}</a>'.format(MAILTO_EMAIL),
        )

    for m in LINK_RE.finditer(text):
        out.append(_bold_and_italic(text[pos:m.start()]))
        link_text, url = m.group(1), m.group(2)
        out.append(
            '<a href="{0}">{1}</a>'.format(escape(url), _bold_and_italic(link_text))
        )
        pos = m.end()
    out.append(_bold_and_italic(text[pos:]))
    return "".join(out)


def render_markdown(md_text: str) -> str:
    lines = md_text.splitlines()
    html_parts = []
    i = 0
    n = len(lines)
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append("  </ul>")
            in_list = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped == "":
            i += 1
            continue

        if stripped.startswith("# "):
            close_list()
            html_parts.append("<h1>" + inline_format(stripped[2:].strip()) + "</h1>")
            i += 1
            continue

        if stripped.startswith("## "):
            close_list()
            html_parts.append("<h2>" + inline_format(stripped[3:].strip()) + "</h2>")
            i += 1
            continue

        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("- ") and not stripped.startswith("**"):
            # A standalone italic line, e.g. *Effective September 28, 2026*
            close_list()
            html_parts.append('<p class="effective-date">' + inline_format(stripped) + "</p>")
            i += 1
            continue

        if stripped.startswith("- "):
            if not in_list:
                html_parts.append("  <ul>")
                in_list = True
            item_lines = [stripped[2:].strip()]
            i += 1
            # Gather indented continuation lines belonging to this item.
            while i < n:
                cont = lines[i]
                if cont.strip() == "":
                    break
                if cont.startswith("  ") and not cont.strip().startswith("- "):
                    item_lines.append(cont.strip())
                    i += 1
                else:
                    break
            item_text = " ".join(item_lines)
            html_parts.append("    <li>" + inline_format(item_text) + "</li>")
            continue

        # Paragraph: gather following non-blank, non-special lines.
        close_list()
        para_lines = [stripped]
        i += 1
        while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(("# ", "## ", "- ")):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        html_parts.append("  <p>" + inline_format(para_text) + "</p>")

    close_list()
    return "\n".join(html_parts)


def build_page(page: dict) -> None:
    md_text = page["markdown"].read_text(encoding="utf-8")
    body_html = render_markdown(md_text)

    # The document's own "# Heading" and its italic effective-date line move
    # into the teal page header; the rest stays in the article body.
    heading = escape(page["title"])
    m = re.search(r"<h1>(.*?)</h1>\n?", body_html)
    if m:
        heading = m.group(1)
        body_html = body_html[:m.start()] + body_html[m.end():]
    effective = ""
    m = re.search(r'<p class="effective-date">.*?</p>\n?', body_html)
    if m:
        effective = m.group(0).strip()
        body_html = body_html[:m.start()] + body_html[m.end():]

    page_html = PAGE_TEMPLATE.format(
        title=escape(page["title"]),
        description=escape(page["description"]),
        path=page["path"],
        heading=heading,
        effective=effective,
        body=body_html,
    )
    page["output"].parent.mkdir(parents=True, exist_ok=True)
    page["output"].write_text(page_html, encoding="utf-8")
    print("Wrote", page["output"].relative_to(SITE_ROOT))


def main() -> None:
    for page in PAGES:
        build_page(page)


if __name__ == "__main__":
    main()
