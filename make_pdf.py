#!/usr/bin/env python3
"""Combine multiple Markdown files into a single PDF.

Usage:
    make_pdf.py [--dir DIR] [--output OUT] [--include-readme] [md_files ...]

Without explicit md_files, recursively collects every ``*.md`` under ``--dir``
(default ``docs/``), skipping ``README.md`` (unless ``--include-readme``) and any
file inside a ``patches/`` directory.
"""

import argparse
import glob
import sys
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML
except ImportError as exc:
    sys.exit(
        f"Missing dependency ({exc.name}). Install with:\n"
        "  pip install markdown weasyprint"
    )


CSS = """
@page {
    size: A4;
    margin: 2cm 1.8cm;
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #888;
    }
}

body {
    font-family: "DejaVu Sans", sans-serif;
    font-size: 10pt;
    line-height: 1.45;
    color: #222;
}

h1 { font-size: 18pt; margin: 0 0 0.5em; border-bottom: 2px solid #333; padding-bottom: 0.2em; }
h2 { font-size: 14pt; margin: 1.2em 0 0.4em; border-bottom: 1px solid #ccc; padding-bottom: 0.15em; }
h3 { font-size: 12pt; margin: 1em 0 0.3em; }
h4, h5, h6 { font-size: 10.5pt; margin: 0.8em 0 0.2em; }

p { margin: 0.4em 0; }

a { color: #1a0dab; text-decoration: none; }

code {
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 9pt;
    background: #f4f4f4;
    padding: 0 0.2em;
    border-radius: 2px;
}

pre {
    font-family: "DejaVu Sans Mono", monospace;
    font-size: 8.5pt;
    background: #f6f6f6;
    border: 1px solid #ddd;
    padding: 0.5em;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
pre code { background: none; padding: 0; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.6em 0;
    font-size: 9pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 0.3em 0.5em;
    text-align: left;
    vertical-align: top;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
th { background: #eee; }

blockquote {
    margin: 0.5em 0;
    padding: 0.1em 1em;
    border-left: 4px solid #ccc;
    color: #555;
}

hr { border: none; border-top: 1px solid #ccc; margin: 1em 0; }

ul, ol { margin: 0.4em 0 0.4em 1.2em; padding: 0; }
li { margin: 0.15em 0; }

.doc-section { page-break-before: always; }
.doc-section:first-of-type { page-break-before: auto; }
.doc-title { font-size: 20pt; color: #111; border-bottom: 3px solid #111; }
.doc-source { font-size: 8pt; color: #888; margin-bottom: 1em; }
"""


def collect_from_dir(root: Path, include_readme: bool) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"Error: lookup directory not found: {root}")

    files = []
    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if any(part == "patches" for part in rel_parts):
            continue
        if any(part.startswith(".") for part in rel_parts):
            continue
        if not include_readme and path.name == "README.md":
            continue
        files.append(path)
    return files


def collect_from_args(paths: list[str]) -> list[Path]:
    files = []
    for raw in paths:
        matches = [Path(p) for p in glob.glob(raw, recursive=True)]
        if not matches:
            print(f"Warning: no files match '{raw}'", file=sys.stderr)
            continue
        for p in matches:
            if p.suffix.lower() != ".md":
                print(f"Warning: skipping non-markdown file '{p}'", file=sys.stderr)
                continue
            if not p.is_file():
                print(f"Warning: file not found: '{p}'", file=sys.stderr)
                continue
            files.append(p)
    return files


def render_doc(paths: list[Path]) -> str:
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "toc"]
    )

    parts = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"Warning: could not read '{path}': {exc}", file=sys.stderr)
            continue

        md.reset()
        body = md.convert(text)
        parts.append(
            '<section class="doc-section">'
            f'<h1 class="doc-title">{path.name}</h1>'
            f'<div class="doc-source">{path}</div>'
            f"{body}</section>"
        )

    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{CSS}</style></head><body>"
        + "\n".join(parts)
        + "</body></html>"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Combine Markdown files into a single PDF."
    )
    parser.add_argument(
        "--dir",
        default="docs",
        help="Directory to scan recursively for *.md (default: docs/). "
        "Ignored when explicit files are given.",
    )
    parser.add_argument(
        "--output",
        default="combined.pdf",
        help="Output PDF path (default: combined.pdf).",
    )
    parser.add_argument(
        "--include-readme",
        action="store_true",
        help="Include README.md when scanning a directory.",
    )
    parser.add_argument(
        "md_files",
        nargs="*",
        help="Explicit .md files or globs to include (overrides --dir).",
    )
    args = parser.parse_args()

    if args.md_files:
        paths = collect_from_args(args.md_files)
    else:
        paths = collect_from_dir(Path(args.dir), args.include_readme)

    if not paths:
        sys.exit("Error: no markdown files found.")

    html = render_doc(paths)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(str(out))

    print(f"Combined {len(paths)} file(s) into {out}")
    for p in paths:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
