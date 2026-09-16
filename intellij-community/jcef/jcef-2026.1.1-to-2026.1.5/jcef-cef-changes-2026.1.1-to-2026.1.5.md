# JCEF/CEF Changes in IntelliJ Community

## Range

`idea/2026.1.1..idea/2026.1.5`

Source repository: [JetBrains/intellij-community](https://github.com/JetBrains/intellij-community)

## Scope & Methodology

The tag range contains **972 commits**. Each commit's changed paths and subject
were scanned for JCEF/CEF relevance using path-segment matching (`/jcef/`,
`/cef/`, `jcef` in file names) and keyword matching on commit subjects
(`jcef`, `cef`, `chromium`, `browser`).

Exactly **3 commits** touch JCEF/CEF-related code. The JCEF library itself is
unchanged: both tags resolve to `org/jetbrains/intellij/deps/jcef/jcef/137/jcef-137.jar`
(`libraries/jcef/module-content.yaml`), so there is no CEF binary/native
version bump in this range.

The **JetBrains Runtime (JBR)** `runtimeBuild` dependency is also tracked in
this report: it was promoted by 4 bot commits (see the "JetBrains Runtime (JBR)
update" section below), though it carries no CEF version change.

## Summary

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 1 | `f07d1eb5` | 2026-04-19 | IJPL-242830 | Check whether CEF version was updated | `JBCefApp.java`, `JBCefNotifications.java`, `IdeBundle.properties` |
| 2 | `5b9a22f3` | 2026-04-27 | IJPL-242830 | Clear jcef caches in OSX for version 2026.1.2 | `JBCefApp.java` |
| 3 | `71cb2829` | 2026-05-07 | IJPL-171896 | Markdown preview doesn't render images from outside the project | `FileSchemeResourcesProcessor.kt`, `IncrementalDOMBuilder.kt` |

## Detail

### 1. `f07d1eb5` — IJPL-242830 "Check whether CEF version was updated"

Author: Artem Bochkarev
Cherry-picked from `c8500066`.

**What / why:** Introduces automatic `jcef_cache` folder cleanup when the CEF
runtime version changes (CEF 137 in this release). When a version bump is
detected, JBCef starts with a temporary cache folder while the old cache is
deleted in a background thread. If deletion fails, the user is shown a warning
notification with the cache path.

**Changes:**
- `platform/ui.jcef/jcef/JBCefApp.java`
  - New constants `SETTINGS_CEF_VERSION_KEY`, `SETTINGS_CEF_TEMP_CACHE_KEY`,
    `SETTINGS_CEF_VERSION_DEFAULT_VAL` (137).
  - New `checkCEFVersionUpdate(CefSettings)` invoked during `JBCefApp`
    construction; swaps `settings.cache_path` to `jcef_cache_temp`, schedules
    background deletion, and cleans up any leftover temporary cache from a
    previous interrupted run.
  - Refactors version detection into a cached `getVersionDetails()` helper and
    reuses it in the support check.
- `platform/ui.jcef/jcef/JBCefNotifications.java`
  - New `showClearCache(Path)` warning notification.
- `platform/platform-api/resources/messages/IdeBundle.properties`
  - New message keys `notification.content.jcef.clearcache.title` and
    `notification.content.jcef.clearcache.message`.

### 2. `5b9a22f3` — IJPL-242830 "Clear jcef caches in OSX for version 2026.1.2"

Author: Artem Bochkarev

**What / why:** One-time forced cache cleanup targeted at macOS users on the
`2026.1.2` build. Because the CEF version did not change, the version-change
heuristic from commit #1 would not trigger; this adds a build-version-based
condition so the cache is cleared once for affected macOS installs.

**Changes:**
- `platform/ui.jcef/jcef/JBCefApp.java`
  - New `SETTINGS_IS_CLEARED_2026_1_2` property flag.
  - `checkCEFVersionUpdate` now also clears the cache when running on macOS,
    full version starts with `2026.1.2`, and the flag is not yet set
    (`doClearCacheFor2026_1_2`), persisting the flag afterwards.

### 3. `71cb2829` — IJPL-171896 "Markdown preview doesn't render images from outside the project"

Author: Ilia Permiashkin (co-authored by Peter Gromov)
Cherry-picked from `c1109fac`.

**What / why:** Markdown preview rendered inline images referenced from outside
the project as external resources incorrectly. The file-scheme resource
processor was rewritten to resolve paths via NIO (`toNioPathOrNull`) instead of
`URL`/`File`, and to honor trusted-project rules when resolving out-of-project
images.

**Changes:**
- `plugins/markdown/core/src/org/intellij/plugins/markdown/ui/preview/jcef/impl/FileSchemeResourcesProcessor.kt`
  - `loadResource` now builds a `Path`, refreshes via
    `VirtualFileManager.refreshAndFindFileByNioPath` for in-project resources,
    and falls back to loading external files directly when outside the project
    root.
- `plugins/markdown/core/src/org/intellij/plugins/markdown/ui/preview/jcef/impl/IncrementalDOMBuilder.kt`
  - New `findRelativePath` helper and trusted-project guard
    (`TrustedProjects.isProjectTrusted`) gating out-of-project image loading;
    path normalization via `toNioPathOrNull().normalize()`.

## JetBrains Runtime (JBR) update

The `runtimeBuild` dependency (the bundled JetBrains Runtime) was promoted by
four `runtime-promotion-bot-noreply` commits (all `IJI-3336`), each a single
line in `build/dependencies/dependencies.properties`:

| # | Commit | Date | From | To |
|---|--------|------|------|----|
| 4 | `21e28680d4a3` | 2026-04-21 | 25.0.2b329.111 | 25.0.2b329.117 |
| 5 | `2c3a1abc3bb7` | 2026-04-29 | 25.0.2b329.117 | 25.0.2b329.123 |
| 6 | `05dfc9c5f742` | 2026-05-09 | 25.0.2b329.123 | 25.0.3b329.124 |
| 7 | `239e49921edf` | 2026-08-03 | 25.0.3b329.124 | 25.0.4b329.128 |

Net effect: `runtimeBuild` `25.0.2b329.117` → `25.0.4b329.128` (JBR 25.0.2 →
25.0.4).

**Relationship to JCEF/CEF:** JBR is the delivery vehicle for the native CEF —
`JBCefApp` selects the native source via `isJcefFromJbr()` (CEF bundled in JBR
vs. a standalone native bundle). These JBR patch releases carried **no CEF
version change**, however: CEF remained 137 (`jcef-137.jar`) in both tags. The
two IJPL-242830 commits (#1/#2) are the JCEF-side cache-management logic that
reacts to a CEF version change arriving via JBR; because the CEF version stayed
constant here, commit #2 was added as a build-version-gated macOS workaround.

## Risk / Impact Assessment

- **Commits #1 & #2** alter JCEF startup caching behavior. The logic is guarded
  by version/build checks and `PropertiesComponent` flags, so the cache-clear
  path is bounded to a single trigger condition. The main risk is an unexpected
  cache wipe if the `2026.1.2` macOS condition is ever mis-evaluated; the flag
  prevents repeated clearing.
- **Commit #3** changes markdown preview image resolution. It tightens security
  by refusing untrusted out-of-project images, which is a behavior improvement
  but could regress legitimate external-image rendering in untrusted projects.
- **JBR update (#4–#7)** bumps the bundled JetBrains Runtime 25.0.2 → 25.0.4
  with no CEF version change. Low JCEF-specific risk, but the runtime promotion
  can introduce unrelated JBR behavior changes.

## Artifacts

- `patches/0001-IJPL-242830-check-cef-version.patch`
- `patches/0002-IJPL-242830-clear-caches-macos.patch`
- `patches/0003-IJPL-171896-markdown-images.patch`
- `patches/0004-IJI-3336-jbr-25.0.2b329.117.patch`
- `patches/0005-IJI-3336-jbr-25.0.2b329.123.patch`
- `patches/0006-IJI-3336-jbr-25.0.3b329.124.patch`
- `patches/0007-IJI-3336-jbr-25.0.4b329.128.patch`
- `patches/combined-2026.1.1-to-2026.1.5.patch`
