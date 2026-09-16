# docs

Change analyses of JetBrains open-source repositories. Each analysis tracks a
tag range, documents what changed in a given area, and ships the corresponding
patches.

## Contents

Currently covers **JCEF/CEF** in
[JetBrains/intellij-community](https://github.com/JetBrains/intellij-community):

```
intellij-community/
└── jcef/
    ├── jcef-2026.1.1-to-2026.1.5/
    │   ├── jcef-cef-changes-2026.1.1-to-2026.1.5.md
    │   └── patches/
    │       ├── 0001-IJPL-242830-check-cef-version.patch
    │       ├── 0002-IJPL-242830-clear-caches-macos.patch
    │       ├── 0003-IJPL-171896-markdown-images.patch
    │       ├── 0004-IJI-3336-jbr-25.0.2b329.117.patch
    │       ├── 0005-IJI-3336-jbr-25.0.2b329.123.patch
    │       ├── 0006-IJI-3336-jbr-25.0.3b329.124.patch
    │       ├── 0007-IJI-3336-jbr-25.0.4b329.128.patch
    │       └── combined-2026.1.1-to-2026.1.5.patch
    └── jcef-2026.1.5-to-2026.2.2/
        ├── jcef-cef-changes-2026.1.5-to-2026.2.2.md
        └── patches/
            ├── 0001-cef-144-and-native-bundles.patch
            ├── 0002-jcef-content-modules-refactor.patch
            ├── 0003-platform-jcef-runtime-fixes.patch
            ├── 0004-markdown-jcef-preview.patch
            ├── 0005-jupyter-python-cef-consumers.patch
            ├── 0006-jbr-runtimebuild-update.patch
            └── combined-2026.1.5-to-2026.2.2.patch
```

## Artifacts

| File | Purpose |
|------|---------|
| `*-changes-<base>-to-<target>.md` | Human-readable report: scope, methodology, commit tables, per-theme detail, risk assessment. |
| `000N-*.patch` | Per-commit diffs grouped by theme, for review/reference only (not a single apply-able diff). |
| `combined-<base>-to-<target>.patch` | Apply-able net diff of the JCEF/CEF paths between the two tags. |

## Quick steps to apply changes

The `combined-*.patch` files are net diffs generated with
`git diff <base> <target> -- <jcef/cef paths>` and apply cleanly to a checkout of
the corresponding **base** tag.

```bash
# 1. Clone the source repository (full history)
git clone https://github.com/JetBrains/intellij-community
cd intellij-community

# 2. Check out the base tag of the report you want to apply
#    e.g. base tag idea/2026.1.5 for the 2026.1.5 -> 2026.2.2 report
git checkout idea/2026.1.5

# 3. Apply the combined patch
git apply path/to/docs/intellij-community/jcef/jcef-2026.1.5-to-2026.2.2/patches/combined-2026.1.5-to-2026.2.2.patch

# 4. Review the result
git status
git diff --stat
```

For the `2026.1.1 -> 2026.1.5` report, use base tag `idea/2026.1.1` and
`combined-2026.1.1-to-2026.1.5.patch`.

> Note: the combined patch covers the JCEF/CEF source paths. A few changes in
> shared/non-JCEF-named files (e.g. `AboutDialog.java`, `dependencies.properties`)
> are documented in the report and theme patches but are not part of the net diff
> because those files are also modified by unrelated commits in the range.

## How reports are produced

For each tag range the full commit set is scanned for JCEF/CEF relevance using
path-segment matching (`/jcef/`, `jcef`/`Jcef`/`Cef`/`CEF` in file names) and
keyword matching on commit subjects. Relevant commits are grouped by theme,
documented in the report, and exported as patches (theme patches =
`git diff <sha>^ <sha>` per commit; combined patch =
`git diff <base> <target> -- <paths>`). See each report's "Scope & Methodology"
section for the exact criteria and exclusions.
