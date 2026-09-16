# JCEF/CEF Changes in IntelliJ Community

## Range

`idea/2026.1.5..idea/2026.2.2`

Source repository: [JetBrains/intellij-community](https://github.com/JetBrains/intellij-community)

## Scope & Methodology

The tag range contains **15,456 commits** (spans the 2026.1 → 2026.2 development
cycle). Each commit's changed paths and subject were scanned for JCEF/CEF
relevance using path-segment matching (`/jcef/`, `jcef`/`Jcef`/`Cef`/`CEF` in
file names) and keyword matching on commit subjects (`jcef`, `cef`, `chromium`,
`browser`).

**45 commits** authored in 2026 were selected and grouped into five themes.
Unlike the earlier `2026.1.1..2026.1.5` analysis (3 commits), this range
contains a CEF version bump, a large JCEF module re-organization, and many
consumer-level fixes.

Excluded (see *Exclusions* below): the Mermaid plugin monorepo merge
(IJPL-245868, which brought ~635 commits of 2022–2024 plugin history), and
build-only noise (Buildifier reformatting, generated build files, Kotlin/compiler
bumps) that merely touched `jcef` `BUILD.bazel`/`.iml` files.

## CEF / JCEF version summary

- **CEF version bumped 137 → 144.** `libraries/jcef/module-content.yaml`:
  - `idea/2026.1.5`: `.../jcef/jcef/137/jcef-137.jar`
  - `idea/2026.2.2`: `.../jcef/jcef/144/jcef-144.jar`
- **Native JCEF now versioned independently of the platform.**
  `build/dependencies/dependencies.properties` gains a `jcefBuild` property that
  was absent in 2026.1.5:
  - `idea/2026.1.5`: *(no `jcefBuild` entry)*
  - `idea/2026.2.2`: `jcefBuild=262-b37`

This reflects the move to shipping JCEF as a **bundled plugin with its own
native bundles** (IJPL-203516 / IJPL-246446) instead of relying solely on the
CEF bundled inside the JetBrains Runtime.

## Relationship to JetBrains Runtime (JBR)

JBR (the JetBrains Runtime, a JDK fork) is the delivery vehicle for the native
CEF. `JBCefApp` decides the native source via `isJcefFromJbr()`: CEF is loaded
either *from JBR* or from the new standalone native bundle
(`JBCefNativeBundleProvider` EP / `getNativeBundlePath()`).

Relevant observations in this range:

- CEF 144 itself ships inside JBR; the Java JCEF library (`jcef-144.jar`) must
  match the CEF bundled in the runtime.
- `jcefBuild=262-b37` now tracks the native JCEF build **separately** from JBR,
  supporting the "JCEF as bundled plugin" architecture that decouples JCEF
  native bits from the runtime.
- Three commits explicitly bridge JBR ↔ JCEF (covered under Theme 3):
  `f71f3c90ddde` (macOS in-process startup from JBR bundle),
  `d7d8ffb3698a` (AboutDialog JCEF version format),
  `d0ce76efee44` (native-bundle-provider priority).
- Generic JBR *version* updates are **not** JCEF/CEF changes: the `runtimeBuild`
  (JBR 25.0.x) and `jdkBuild` (compilation JDK) promotions, the standard/
  lightweight JBR flavour merge, and JBRResolver/installer work are all unrelated
  to JCEF. These are documented separately in the "JetBrains Runtime (JBR)
  update" section below.

## JetBrains Runtime (JBR) update

The bundled JetBrains Runtime dependency was promoted across the range
(`build/dependencies/dependencies.properties`):

| Property | 2026.1.5 | 2026.2.2 | Change |
|----------|----------|----------|--------|
| `runtimeBuild` (JBR) | `25.0.4b329.128` | `25.0.4b508.27` | ~24 `runtime-promotion-bot-noreply` commits (IJI-3336), incl. one revert |
| `jdkBuild` (compiler JDK) | `21.0.10b1163.108` | `25.0.2b410.29` | `aa1cfa9632ab` IJPL-221307 "switch compilation JDK to JBR 25" |

**Relationship to JCEF/CEF:** these JBR promotions carry **no CEF version
change** — the CEF 137→144 transition is tracked independently via
`jcefBuild=262-b37` (see Theme 1). `libraries/jbr/module-content.yaml` is
unchanged (`jbr-api-1.jar` in both tags). The JCEF↔JBR bridge commits remain the
three Theme 3 entries (`f71f3c90ddde`, `d7d8ffb3698a`, `d0ce76efee44`).

## Summary

| Theme | Commits | Key issues |
|-------|---------|------------|
| 1. CEF 137→144 + native bundles | 10 | IJPL-203516, IJPL-243802, IJPL-244083 |
| 2. JCEF content-modules refactor | 9 | IJPL-246446, IJPL-248275 |
| 3. Platform JCEF runtime fixes | 11 | IJPL-224692, IJPL-243323, IJPL-244340, IJPL-243940, IJPL-231223, IJPL-242830, IJPL-231717, IJPL-247041, IJPL-247121 |
| 4. Markdown JCEF preview | 11 | IJPL-91133, IJPL-236346, IJPL-171896, IJPL-92401, IJPL-243436, IJPL-245222, IJPL-250785, IJPL-251259 |
| 5. Jupyter/Python CEF consumers | 4 | PY-89532, IJPL-250575, PY-91405, PY-91324 |

## Theme 1 — CEF 137→144 and native bundles

The JCEF native library is repackaged as a dedicated plugin (`plugins/jcef`)
with its own native bundles, then updated through several milestones ending at
CEF 144 (`262-b37`).

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 1 | `e79a28c88a0a` | 2026-02-11 | IJPL-203516 | Build JCEF plugin with native bundles | `plugins/jcef/plugin/**`, `PluggableCefNativeBundleProvider.kt`, build scripts, `dependencies.properties` |
| 2 | `706518f3193f` | 2026-02-11 | IJPL-203516 | Update product layouts | `community-resources/.../IdeaPlugin.xml`, `plugins/jcef/plugin/**` |
| 3 | `ebb02febf5f7` | 2026-02-11 | IJPL-203516 | Packaging | `plugins/jcef/plugin/**`, product layout scripts |
| 4 | `ab95d6a814a1` | 2026-04-17 | IJPL-203516 | Log info on JCEF loading | `platform/ui.jcef/jcef/JBCefApp.java` |
| 5 | `c2615ea3add1` | 2026-04-17 | IJPL-203516 | update jcef | `lib/BUILD.bazel`, `lib/MODULE.bazel`, `libraries/jcef/...iml` |
| 6 | `cccb636e4ee3` | 2026-04-19 | IJPL-203516 | Update JCEF for plugin 262-b28 | `dependencies.properties` |
| 7 | `139175dd2721` | 2026-04-20 | IJPL-203516 | Enable executable flags for MacOS | `CommunityRepositoryModules.kt` |
| 8 | `e8d921349b60` | 2026-04-28 | IJPL-243802 | Switch to CEF 144 | `dependencies.properties`, `lib/**`, `libraries/jcef/module-content.yaml`, `api-dump*.txt`, `JBCefStreamResourceHandler.kt`, `MyResourceHandler.kt` |
| 9 | `5ba8ab1cfe37` | 2026-05-04 | IJPL-244083 | Adapt MarkdownPreviewSecurityTest to CEF 144 | `MarkdownPreviewSecurityTest.kt` |
| 10 | `41beba2fb941` | 2026-05-05 | IJPL-203516 | update jcef to 262b37 | `dependencies.properties`, `lib/**`, `libraries/jcef/...iml` |

**Key changes:** introduces the `intellij.jcef` plugin and
`PluggableCefNativeBundleProvider`, wires the plugin into product layouts,
bumps the bundled JCEF dependency in `lib/MODULE.bazel`, and finally switches the
library from CEF 137 to CEF 144 in `libraries/jcef/module-content.yaml`. The
CEF-144 switch also refreshes the `ui.jcef` API dumps and adapts
`JBCefStreamResourceHandler` / the resource-handler test to the new CEF.

## Theme 2 — JCEF content-modules refactor (IJPL-246446, IJPL-248275)

The JCEF UI is split out of `platform/platform-impl` into dedicated **content
modules** and the JCEF API is published as a bundled library plugin, making
JCEF-dependent features optional.

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 11 | `6cb976acd581` | 2026-06-05 | IJPL-246446 | publish JCEF API as a bundled library plugin | `libraries/jcef/plugin/**`, `plugins/jcef/plugin/**`, module-set scripts |
| 12 | `b6c05fe0b33e` | 2026-06-05 | IJPL-246446 | add optional platform extension points for JCEF UI | `HwFacade*`, `FocusedComponentProvider`, `ProxySettingsListener` → `platform-api`; `ui.jcef` impls |
| 13 | `6a73540d5058` | 2026-06-05 | IJPL-246446 | move platform JCEF UI into content modules | moves ~80 JCEF UI/test files into `platform/platform-impl/jcef/**` and `platform/platform-impl/internal/jcef/**` |
| 14 | `094dd0278964` | 2026-06-05 | IJPL-246446 | extract onboarding browser rendering to JCEF module | `platform/new-ui-onboarding/jcef/**` |
| 15 | `ba30652e5258` | 2026-06-05 | IJPL-246446 | wire JCEF content modules into products | generated module sets, `PlatformExtensionPoints.xml`, plugin descriptors |
| 16 | `416874153a22` | 2026-06-08 | IJPL-246446 | split JCEF remote driver module | `plugins/performanceTesting/remote-driver.jcef/**` |
| 17 | `224b2ab72b50` | 2026-06-08 | IJPL-246446 | Fold JCEF modules into existing plugin | module-set/product-layout scripts, `intellij.libraries.jbr.xml`, MPS/PyCharm props |
| 18 | `f2c673e84591` | 2026-06-22 | IJPL-246446 | fix demo actions | `intellij.internal.jcef.xml` |
| 19 | `85ff6391a960` | 2026-06-24 | IJPL-248275 | Make JCEF-dependent content modules optional | `images/jcef/**` (JCefImageViewer), `plugins/markdown/jcef/**` split from `markdown/core` |

**Key changes:** establishes `libraries/jcef/plugin` (bundled library plugin),
moves platform JCEF UI and internal JCEF test cases into content modules,
extracts onboarding (New UI) browser rendering and the image viewer into their
own JCEF modules, splits the Markdown JCEF preview into `plugins/markdown/jcef`,
and makes all of these optional so products can omit JCEF-dependent features.

## Theme 3 — Platform JCEF runtime fixes

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 20 | `6131d90e76b2` | 2026-04-19 | IJPL-231717 | Don't set new CefAppHandler before jcef restart | `JBCefApp.java` |
| 21 | `1dd73654b7da` | 2026-04-19 | IJPL-242830 | Check whether CEF version was updated | `JBCefApp.java`, `JBCefNotifications.java`, `IdeBundle.properties` |
| 22 | `d7d8ffb3698a` | 2026-04-22 | IJPL-231223 | AboutDialog: fix JBR with JCEF version format | `AboutDialog.java` |
| 23 | `3ec1c4fc6f20` | 2026-04-27 | IJPL-224692 | allow sandbox on mac for out-of-process | `SettingsHelper.java` |
| 24 | `d0ce76efee44` | 2026-04-27 | IJPL-224692 | prioritize JBCefDefaultNativeBundleProvider | `PlatformExtensions.xml` |
| 25 | `b29db5f88206` | 2026-04-29 | IJPL-243323 | JCEF enabled in plugins but unavailable in RD | `plugins/jcef/frontend/**`, `plugins/jcef/plugin/**` |
| 26 | `f71f3c90ddde` | 2026-05-06 | IJPL-244340 | restore macOS in-process JCEF startup with bundled JBR | `JBCefApp.java` |
| 27 | `b87fbfdb2299` | 2026-05-18 | IJPL-243940 | run jcef with `--ozone-platform=x11` on wayland | `SettingsHelper.java` |
| 28 | `990bf9faa332` | 2026-06-11 | IJPL-247041 | make Web Browser action available in RemDev | `plugins/jcef/frontend/**` |
| 29 | `e3db588246bb` | 2026-06-29 | IJPL-247121 | Incorrect suggestion to update Web Browser (JCEF) plugins | `IdeaPluginOsRequirement.kt`, `PluginCpuArchRequirement.kt`, `PluginManagerCore.kt`, tests |
| 30 | `75d2ba295445` | 2026-07-03 | IJPL-247121 | (follow-up) | `PluginManagerCore.kt` |

**Key changes:** `1dd73654b7da` ports the CEF-version cache-cleanup logic to
master (the release-branch cherry-pick `f07d1eb5` was covered in the previous
report). `f71f3c90ddde` restores macOS in-process JCEF startup by locating the
CEF framework and `jcef Helper` app inside the JBR bundle.
`3ec1c4fc6f20`/`d0ce76efee44` enable the macOS sandbox for out-of-process JCEF
and fix native-bundle-provider priority. `b29db5f88206` fixes JCEF availability
detection in remote development. `b87fbfdb2299` forces the X11 ozone platform on
Wayland. `e3db588246bb`/`75d2ba295445` add OS/CPU-arch requirement checks so the
IDE stops suggesting incompatible updates for the Web Browser (JCEF) plugin.

## Theme 4 — Markdown JCEF preview

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 31 | `06c2304250ab` | 2026-04-07 | IJPL-91133 | Fix OSR scroll speed (scrollAmount) | `JBCefOsrComponent.java`, `registry.properties` |
| 32 | `a3e9217e378e` | 2026-04-14 | IJPL-236346 | Fix HTML export losing styles after jsoup 1.21.2 | `HtmlExporter.kt` |
| 33 | `f8b412146908` | 2026-04-15 | IJPL-91133 | Fix JCEF OSR mouse wheel scroll speed | `JBCefOsrComponent.java`, `registry.properties` |
| 34 | `87fba5d14334` | 2026-04-27 | IJPL-171896 | Markdown preview doesn't render images from outside the project | `FileSchemeResourcesProcessor.kt`, `IncrementalDOMBuilder.kt` |
| 35 | `50a115416c68` | 2026-04-30 | IJPL-171896 | Support all types of path variants | `FileSchemeResourcesProcessor.kt`, `IncrementalDOMBuilder.kt` |
| 36 | `b2b4aefe867c` | 2026-05-05 | IJPL-92401 | run commands with project's root directory | `CommandRunnerExtension.kt`, `MarkdownRunLineMarkersProvider.kt` |
| 37 | `9c71c714f53c` | 2026-05-13 | IJPL-243436 | Add gutter run configuration for runnable JVM classes | markdown command-runner + `plugins/markdown/java/**` |
| 38 | `63eebf03539f` | 2026-06-03 | IJPL-245222 | session-based hashing, prevent `data-command` link propagation | `processLinks.js`, `CommandRunnerExtension.kt` |
| 39 | `8a5f6071a159` | 2026-07-21 | IJPL-245222 | Update clickjacking checks & command confirmation | `CommandRunnerExtension.kt`, `commandRunner.js/css`, `MarkdownBundle.properties` |
| 40 | `e2a6d9082df2` | 2026-08-03 | IJPL-250785 | High CPU from run-configuration lookups per code span | `MarkdownRunLineMarkersProvider.kt` |
| 41 | `caef43e423f0` | 2026-08-17 | IJPL-251259 | Adapt scrollbar styling to IDE scale | `JBCefScrollbarsHelper.java` |

**Key changes:** fixes OSR mouse-wheel scroll speed in the shared
`JBCefOsrComponent` (benefiting all OSR consumers), repairs Markdown HTML export
after the jsoup upgrade, hardens the preview against out-of-project images and
clickjacking (`data-command` link propagation), adds JVM run-configuration
gutter actions for fenced code, and reduces CPU from per-code-span
run-configuration lookups. Note that commits 34/35 touch the *old*
`plugins/markdown/core/.../jcef/impl/` paths before the Theme 2 refactor moved
them to `plugins/markdown/jcef/`.

## Theme 5 — Jupyter/Python CEF consumers

| # | Commit | Date | Issue | Title | Files |
|---|--------|------|-------|-------|-------|
| 42 | `dc63d7121c3d` | 2026-05-06 | PY-89532 | Jupyter: rewrite CEF sync to v2 | `JcefOffScreenViewComponentUi.kt` (remote-driver test SDK) |
| 43 | `ddd7464712dc` | 2026-07-20 | IJPL-250575 | Scroll trap on the What's New page | `SettingsHelper.java`, `registry.properties` |
| 44 | `a1136dd7a9a4` | 2026-08-06 | PY-91405 | WhatsNew Vision/Legacy modes reworked | `PyCharmJcefWhatsNewPatcher.kt`, `PyCharmWhatsNewInVisionContentProvider.kt` |
| 45 | `3a0c99a60710` | 2026-07-30 | PY-91324 | scope PySdkListener updates to owning project | `PyPackagingJcefHtmlPanel.kt` (among Python packaging files) |

**Key changes:** rewrites the Jupyter JCEF off-screen sync to v2, fixes a
scroll trap on the JCEF-rendered What's New page, and reworks the PyCharm
What's New patcher for the new Vision/Legacy modes. Commit 45 is tangential — a
Python packaging tool-window change that only incidentally touches
`PyPackagingJcefHtmlPanel.kt`.

## Exclusions

- **Mermaid monorepo merge (IJPL-245868).** `2ce2ae0bc16c` and
  `5103c4c0f4dd` merged the Mermaid plugin (with its full 2022–2024 history,
  ~635 commits) into the monorepo. ~63 of those historical commits touch JCEF
  paths but predate this range; they are excluded per scope.
- **Build-only noise.** Buildifier reformatting (`2dc4acc8d037`,
  `f6d1e9612a1e`), generated build-file regeneration (`73ae80d35fe7`,
  `6190d7d4b41a`, `963e91cac5fe`, `2107bb3644f0`), Kotlin/compiler bumps
  (`2ec83dbdeb68`, `1469dc64e8b5`, `943d105cc0d5`), and the JPMS library-wrapper
  commits (`338be7036ffa` / `1f3e0d270ba9`) touch `jcef` build files but contain
  no JCEF logic.
- **Generic JBR/runtime updates** (see the "JetBrains Runtime (JBR) update" section).

## Risk / Impact Assessment

- **Theme 1 (CEF 144)** is the highest-impact change: a major Chromium version
  bump. Behavioral/rendering regressions in all JCEF consumers are possible, and
  the API dumps (`api-dump.txt`) changed, indicating an API surface shift. The
  `MarkdownPreviewSecurityTest` adaptation (`5ba8ab1cfe37`) signals that CEF 144
  changed security-handling behavior in Markdown preview.
- **Theme 2 (module refactor)** is primarily structural (code moves into content
  modules) but changes extension points and module dependency wiring. Products
  that relied on JCEF UI being unconditionally present must now opt in; the
  "optional content modules" change (`85ff6391a960`) is the mechanism that makes
  JCEF optional.
- **Theme 3** contains the sandbox/out-of-process and macOS in-process changes
  (`f71f3c90ddde`, `3ec1c4fc6f20`), which touch low-level CEF startup; regressions
  there manifest as JCEF failing to initialize on macOS or in remote development.
- **Themes 4 & 5** are localized consumer fixes with limited blast radius, though
  the Markdown security hardening (`87fba5d14334`, `8a5f6071a159`) intentionally
  restricts what untrusted content can do and could affect legitimate use cases.
- **JBR update** (`runtimeBuild` 25.0.4 patch promotions, `jdkBuild` 21 → 25)
  carries no CEF change and is low JCEF-specific risk; the JBR promotions and the
  JBR 25 compiler-JDK switch can introduce unrelated runtime/build behavior
  changes.

## Artifacts

- `patches/0001-cef-144-and-native-bundles.patch`
- `patches/0002-jcef-content-modules-refactor.patch`
- `patches/0003-platform-jcef-runtime-fixes.patch`
- `patches/0004-markdown-jcef-preview.patch`
- `patches/0005-jupyter-python-cef-consumers.patch`
- `patches/0006-jbr-runtimebuild-update.patch`
- `patches/combined-2026.1.5-to-2026.2.2.patch`
