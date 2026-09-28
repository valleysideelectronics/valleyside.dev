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
        "title": "Privacy Policy — Lake Cumberland",
        "description": "Privacy policy for the Lake Cumberland app, published by Valleyside Electronics LLC.",
    },
    {
        "markdown": SOURCE_DIR / "terms.md",
        "output": SITE_ROOT / "lake-cumberland" / "terms" / "index.html",
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
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="/">Valleyside Electronics LLC</a>
    <nav>
      <a href="/lake-cumberland/">Lake Cumberland app</a>
      <span class="sep">&middot;</span>
      <a href="/support/">Support</a>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  &copy; 2026 Valleyside Electronics LLC
</footer>
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
    page_html = PAGE_TEMPLATE.format(
        title=escape(page["title"]),
        description=escape(page["description"]),
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
