# Desktop Japanese font ROM import validation

Initial feature validation on October 11, 2026, before release packaging.
The font importer is included in Mac/Homebrew 1.0.2. See the separate
[final installer validation](QA-MACOS-1.0.2.md); the checks below retain the
scope and limitations of the earlier local QA build.

## Change

- The Run tab exposes Japanese font ROM import with either emulator backend.
- The portable JNI boot path loads the private `PC110-FONT.rom` copy and
  reports a dedicated boot error if the selected ROM cannot be loaded.
- Import checks the exact 1 MiB size and IBM FONT header. Failed replacement
  preserves the existing private copy. No firmware is bundled or downloaded.
- The optional default argument preserves existing two-argument boot callers.
  JNI binaries must be rebuilt with the updated Kotlin host.

## Checks

- All 28 desktop JVM/native tests passed on Apple silicon with JDK 21.
- Five new font tests cover private-copy import, source preservation, invalid
  first imports, failed replacements, optional-font boot, malformed or missing
  ROM rejection, and recovery after a rejected boot.
- An entirely synthetic BIOS reads the imported ROM aperture and displays a
  color derived from its bytes. The resulting frame survives reset and a fresh
  host instance; replacing the ROM changes the guest's output. These tests use
  no proprietary ROMs or glyphs.
- The native library builds for both arm64 and x86_64 with macOS 12 as the
  deployment target. Intel runtime testing was not performed on this host.
- The rebuilt local macOS app shows the font row under Run > Personal media.
  Clicking it opens the native picker titled
  `Select PC110 Japanese font ROM (1 MiB)`. Cancellation leaves media unchanged.
- The Compose screenshot export completed with isolated media storage.
- The local packaged launcher passed `--smoke-test`, including JNI loading,
  private media copying and rendering all 19 schematic pages.
- Source whitespace checks passed. Existing Compose deprecations and two
  unrelated C string-initializer warnings remain.

## Packaging and remaining release work

The UI-check application is a local, unnotarized build. It uses the available
Homebrew JDK with `-Pcompose.desktop.packaging.checkJdkVendor=false` solely for
local QA. No project setting was changed to disable the packaging vendor check.
Use the established release JDK, signing, notarization and per-architecture
validation workflow before publishing new DMGs and updating the cask.

Genuine Japanese glyph rendering with user-owned PersonaWare media was not
retested here. No installed application or user's imported ROM was replaced,
and no release, cask, or GitHub source update was published by this change.
