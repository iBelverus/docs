# make_pdf.py

Combines multiple Markdown files (e.g. the JCEF/CEF change reports) into a
single PDF using `markdown` and WeasyPrint.

## Environment setup

### Linux / WSL

```bash
# system libraries required by WeasyPrint
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev

# create and activate the virtual environment (from docs/)
python3 -m venv .venv
source .venv/bin/activate

# install Python dependencies (after activation)
pip install markdown weasyprint
```

Deactivate with `deactivate`.

### Windows

1. Install the
   [Python Install Manager](https://apps.microsoft.com/detail/9nq7512cxl7t) from
   the Microsoft Store (provides the `python` command).
2. Install [MSYS2](https://www.msys2.org/#installation) keeping the default
   options.
3. In the MSYS2 **UCRT64** shell, install Pango and its dependencies, then close
   the shell:

   ```bash
   pacman -S mingw-w64-ucrt-x86_64-pango
   ```

4. In a Windows command prompt (`cmd`):

   ```bat
   python -m venv .venv
   .venv\Scripts\activate.bat
   pip install markdown weasyprint
   ```

If you get an error like `cannot load library '...'`, point WeasyPrint at the
MSYS2 DLLs before running the script:

```bat
set WEASYPRINT_DLL_DIRECTORIES=C:\msys64\ucrt64\bin
```

## Usage

All examples assume an activated venv (`source .venv/bin/activate` on
Linux/WSL, `.venv\Scripts\activate.bat` on Windows).

Basic recursive scan (default `--dir docs`, skips `README.md` and `patches/`):

```bash
python make_pdf.py
```

Explicit directory and output path:

```bash
python make_pdf.py --dir intellij-community --output reports.pdf
```

Explicit file list or globs (overrides `--dir`):

```bash
python make_pdf.py intellij-community/jcef/*/*/*.md
python make_pdf.py --output single.pdf intellij-community/jcef/jcef-2026.1.1-to-2026.1.5/*.md
```

Include `README.md` when scanning a directory:

```bash
python make_pdf.py --include-readme
```

## Options

| Option | Description |
|--------|-------------|
| `--dir DIR` | Directory to scan recursively for `*.md` (default: `docs`). Ignored when explicit files are given. |
| `--output OUT` | Output PDF path (default: `combined.pdf`). |
| `--include-readme` | Include `README.md` when scanning a directory. |
| `md_files ...` | Explicit `.md` files or globs to include (overrides `--dir`). |

## Notes

- The output PDF defaults to `combined.pdf` in the current directory.
- Directory mode sorts files depth-first; list mode preserves argument order.
- Non-markdown or missing paths are warned and skipped; if no files are found
  the script exits with an error.
