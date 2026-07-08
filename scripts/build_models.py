#!/usr/bin/env python3
"""Regenerate models.html from the Obsidian "Mental Models" folder.

Usage: python3 scripts/build_models.py

Reads every .md note in the vault folder, strips Obsidian {{ir::...}}
incremental-reading markers, converts the light markdown these notes use
(bold, italics, bullets, bare URLs), and writes models.html in the repo
root. Notes whose filename starts with "todo" and empty notes are skipped.
Entries are ordered alphabetically by title.
"""

import datetime
import html
import re
from pathlib import Path

VAULT = (
    Path.home()
    / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault/Atlas/Mental Models"
)
OUT = Path(__file__).resolve().parent.parent / "models.html"

URL_RE = re.compile(r"https?://[^\s<>\"]+")


def clean_markers(text: str) -> str:
    text = text.replace("{{ir::", "")
    text = text.replace("}}", "")
    return text.strip()


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+?)_(?![\w_])", r"<em>\1</em>", text)
    text = URL_RE.sub(
        lambda m: f'<a href="{m.group(0)}" target="_blank" rel="noopener noreferrer">source ↗</a>',
        text,
    )
    return text


def note_to_html(text: str) -> str:
    """Convert a cleaned note body to HTML blocks."""
    blocks: list[str] = []
    para: list[str] = []
    bullets: list[str] = []

    def flush_para() -> None:
        if para:
            joined = " ".join(para).strip()
            if joined:
                if URL_RE.fullmatch(joined):
                    blocks.append(f'<p class="model-source">{inline_md(joined)}</p>')
                else:
                    blocks.append(f"<p>{inline_md(joined)}</p>")
            para.clear()

    def flush_bullets() -> None:
        if bullets:
            items = "".join(f"<li>{b}</li>" for b in bullets)
            blocks.append(f"<ul>{items}</ul>")
            bullets.clear()

    for raw in text.split("\n"):
        line = raw.strip()
        if re.match(r"^[-*]\s+", line):
            flush_para()
            bullets.append(inline_md(re.sub(r"^[-*]\s+", "", line)))
        elif not line:
            flush_para()
            flush_bullets()
        else:
            flush_bullets()
            para.append(line)
    flush_para()
    flush_bullets()
    return "\n".join(blocks)


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "model"


def main() -> None:
    notes = []
    latest = 0.0
    for path in sorted(VAULT.glob("*.md"), key=lambda p: p.stem.lower()):
        if path.stem.lower().startswith("todo"):
            continue
        body = clean_markers(path.read_text(encoding="utf-8"))
        if not body:
            continue
        notes.append((path.stem, note_to_html(body)))
        latest = max(latest, path.stat().st_mtime)

    updated = datetime.date.fromtimestamp(latest).strftime("%B %Y").lower()
    entries = "\n".join(
        f'''      <article class="model" id="{slugify(title)}">
        <h2>{html.escape(title)}</h2>
{body}
      </article>'''
        for title, body in notes
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>mental models &middot; Ammaar Khan</title>
    <meta
      name="description"
      content="A running library of the mental models Ammaar Khan steers by, collected from books, mentors, and his own experiments."
    />
    <meta property="og:title" content="mental models &middot; Ammaar Khan" />
    <meta
      property="og:description"
      content="A running library of the mental models Ammaar Khan steers by."
    />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://ammaarkhan.com/models.html" />
    <link
      rel="icon"
      href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%91%8B</text></svg>"
    />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,340;0,9..144,400;1,9..144,340;1,9..144,400&family=Karla:ital,wght@0,400;0,500;0,600;1,400&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="styles.css" />
    <link rel="stylesheet" href="models.css" />
  </head>
  <body>
    <div class="glow" aria-hidden="true"></div>
    <div class="grain" aria-hidden="true"></div>

    <main class="models-page">
      <nav class="crumb reveal"><a href="./">&larr; ammaar khan</a></nav>

      <header class="models-hero reveal">
        <h1 class="models-title">mental models</h1>
        <p class="models-lede">
          A running library of the models I steer by, collected from books,
          mentors, and my own experiments.
        </p>
        <p class="models-meta">
          {len(notes)} models &middot; updated {updated}
        </p>
      </header>

{entries}

      <footer class="models-coda">
        <p><a href="./">&larr; back to the front page</a></p>
      </footer>
    </main>
  </body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(notes)} models, updated {updated}")


if __name__ == "__main__":
    main()
