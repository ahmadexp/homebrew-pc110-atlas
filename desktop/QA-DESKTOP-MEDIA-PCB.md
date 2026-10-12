# Desktop media, disk and PCB validation

Date: 2026-10-11. Source/local QA build only, not a release announcement.

This records the earlier feature QA. The later
[Mac 1.0.2 release checks](QA-MACOS-1.0.2.md) cover the signed installers.

## Automated checks

The desktop Gradle test suite passes 40 tests on Apple silicon, including:

- Synthetic guest INT 13h reads of the final sector at 512 MiB plus one sector,
  2 GiB plus one sector, and exactly 4 GiB. Reset and repeated power cycles work.
- Read past end-of-disk is rejected; the native host can boot another image
  after that failure. Over-limit import is rejected before copying and preserves
  the existing disk. Fixtures use sparse files and no proprietary firmware.
- Full iPhone-layout ZIP import, optional MCU dumps and shell images, private
  copies, backups, artwork-only replacement, omitted optional file preservation,
  per-disk CMOS retention/reset, failed-commit rollback and restart recovery.
- Path traversal, absolute paths, duplicate slots, missing required media,
  damaged ZIP, incorrect PNG dimensions, invalid font header, non-sector-aligned
  disk and renamed disk-container rejection. Bounded extraction stops before
  writing an over-limit chunk.
- Camera depth-axis spacing, underside painter order, edge-on handling, actual
  mirrored texture rendering and parity with Android's projection/registration.
- Real-asset top and underside renders for all five boards. PNGs are generated
  under `desktop/build/qa-pcb/` for visual inspection.
- Existing font aperture/reset/relaunch, native lifecycle, keyboard/mouse,
  emulator command/protocol and all 19 schematic page tests remain passing.

The macOS native library also compiles for Intel x86-64, targeting macOS 12.
Intel runtime execution has not been tested on this host. The shared C core's
existing file-loader API is retained; the desktop-only larger-image path uses
the new caller-owned raw-memory attachment API.

## Local UI/build checks

The rebuilt macOS app exposes both ZIP import buttons, the font ROM row, 4 GiB
limit wording, and **3D PCB** for all five boards. The mainboard viewer opens and
renders the corrected stack with camera and visibility controls.

The local app image uses the host JDK with a QA-only packaging vendor-check
override. It is not a signed/notarized release artifact. Before updating the
Homebrew cask, build with the approved release JDK, sign and notarize both Mac
architectures, verify the actual packaged app, and publish matching checksums.

## Limits

- No private PersonaWare or Windows media were used in these new regression
  fixtures. Large-disk sector access is verified, not arbitrary OS compatibility.
- The portable core still has session-only disk behavior and lacks full guest
  audio/Windows 95 support. The [Mac 1.0.2 emulator](MACOS-EMULATION.md) adds a
  separate native backend; its Windows 95 boot evidence and remaining driver
  checks are documented there. The 4 GiB cap is not an unlimited-image promise.
- Windows/Linux emulator command construction accepts the same 4 GiB cap, but a
  physical Windows/Linux full-guest 4 GiB run was not performed on this Mac.
- The initial artwork-only shell in this earlier check has since been replaced
  with interactive console controls. See the later Mac release validation record.
  This is still a flat console, not a free-standing 3D laptop.
