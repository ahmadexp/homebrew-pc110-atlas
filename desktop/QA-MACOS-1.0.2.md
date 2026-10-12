# Mac 1.0.2 release validation

Release validation: October 12, 2026.

This update covers the standalone Intel and Apple silicon Mac/Homebrew edition,
not the separate Mac App Store application or other distribution channels.

## Build and package scope

- Release source: `release/mac-desktop-1.0.2`, app inputs at `2c5eb92` and
  console/runtime inputs at `7553f7f`.
- Native macOS 12 deployment target for the desktop JNI core, emulator and its
  private libraries. Execution checks run on newer macOS, not every supported
  macOS version.
- Eclipse Temurin 21.0.12.1+1-LTS, without the local QA vendor-check override.
- 47 desktop JVM/native tests and 39 packaging regression tests passed locally,
  including the additional UI-error wording regression test.
- Developer ID identity: Ahmad Byagowi, team `TWFK4FAG36`.
- Separate architecture-specific DMGs. No Rosetta requirement for native use.
- No proprietary firmware, installed guest disks or private screenshots in CI
  or public release assets.

## Final installer checks

The practical media, console, PCB and guest checks below are complete. Both
native builds passed in run `38218374867` at `c31dd2d`, including all 47 desktop
tests, 39 packaging tests and packaged guest smoke checks on each architecture.
Both final installers are Developer ID signed, Apple notarized and stapled.
Private run `38221870490` passed final signed-installer verification on clean
native Intel and Apple silicon macOS 15 machines. The verified hashes match
the release assets and Homebrew cask.
The earlier Apple silicon candidate failed startup on clean macOS 15.
Its replacement now passes both on the development Mac and clean macOS 15:
the native runtime was built with the macOS 27 SDK, signed, notarized and stapled,
then tested through its actual installer in private run `38217525152`.

Final DMG SHA-256 values:

- Apple silicon:
  `382437cb5af43cec48708463851126a88885a349d14ecc1cc5223e7c102bb649`.
- Intel:
  `676155ead9ce089b04035f62321af77e2eb3707aa1e3f7fb41350d18ad4e320b`.

Earlier candidate hashes are superseded. Only the final signed and stapled
artifacts listed above are used for this release.

The final check verifies the DMG signature, stapled notarization ticket,
Gatekeeper assessment, application signature, version and native architecture.
It runs the packaged launcher, not a development Gradle process.

The packaged smoke checks cover JNI loading, all 19 schematic pages, Skia,
private media copying and emulator process startup. The guest smoke checks cover
text output, 256-color graphics, Enter/Escape input, non-silent PCM transport,
reset, clean stop, a fresh-process restart, Unicode/comma paths and read-only
demo-media preservation. Audio transport does not prove physical speaker output
or full ESS driver compatibility.

## Fixed during release validation

Final signing exposed an interpreter startup crash caused by a macOS JIT
protection call. The interpreter now omits that call, and the builder rejects
an interpreter binary that still imports it. A regression test checks the
preprocessor guard for Mac interpreter, Mac native JIT and non-Mac builds.
The signed Apple silicon candidate passes packaged startup and guest smoke
checks on the development Mac after this fix. The later clean-machine result
also covers this guard.
The emulator does not receive a JIT entitlement.

The macOS 15 crash was traced to GLib's unguarded weak import of `pipe2`,
introduced in the macOS 27 SDK. GLib must use its existing pipe/fcntl fallback
for the macOS 12 deployment baseline. Both the builder and packager now reject
unreviewed weak system imports. The replacement native Apple silicon runtime
builds successfully with the newer SDK, has no unreviewed weak system imports,
and passes the signed installer checks on clean macOS 15.

The console now uses the iPhone's measured 90-key JIS layout. A fixture generated
from the actual Swift keyboard implementation verifies all 2,880 key/modifier
combinations, as well as all key rectangles. Tests also cover duplicate mouse
button ownership, focus-loss key releases, original key-up scan codes and pen
coordinate clamping. Local UI checks verified the complete console fits the
window, pictured keys control the demo, and full-screen exit/display-only switching
work. Pause/resume and three power cycles pass automated session checks.
The rebuilt app's Pause/Resume controls also responded in live UI testing;
input sent while paused was not replayed on resume.

Invalid BIOS sizes now fail before replacing the working 256 KiB import.
An intentional power-off no longer races a display poll into reporting a crash.

## Practical release checks

- Imported an existing personal iPhone-layout ZIP through the packaged Mac UI.
  The BIOS, Japanese font, two optional MCU files and HDD-1 were recognized.
  Alternative disks and unrelated package files were skipped. Nothing started
  automatically, and imports were disabled while the emulator was running.
- Booted PersonaWare with readable Japanese DOS text. Escape skipped its initial
  pen-calibration prompt. Its desktop and Draw Memo opened, with keyboard and
  guest mouse input responding. The test used an isolated app-private media copy.
  A separate disposable-copy test completed all four pen-calibration corners
  through the native input protocol and returned to the PersonaWare desktop.
- Entered full screen and returned using the visible Exit full screen button.
  Earlier display-only, pause/resume and pictured-key checks also passed.
- Imported a separate custom-shell ZIP. Its overlay appeared in the correct
  position, the existing media remained imported, and the backup directory was
  retained. No private artwork or guest screenshots are published.
- Inspected the mainboard stack and its underside in the live PCB viewer using
  the tilt control. Real-asset renders and automated registration/projection
  tests cover all five boards. Layer edges and mounting holes remain aligned
  through the exploded stack.
- Repeated original-image Windows boot, ScanDisk completion, desktop mouse use,
  all Display Properties pages and normal Windows shutdown without reproducing
  the earlier VMM exception. This is a bounded practical check, not a guarantee
  that the intermittent fault is fixed.

Live drag automation did not establish a reliable pass for the pictured
TrackPoint or pen-pad gesture. Their geometry, coordinate bounds, input routing
and release handling have regression coverage, but this record does not claim
complete manual gesture or iPhone feature parity.

The signing tool also preserves and reseals the checksums of archived emulator
native payloads, and handles optional arguments on macOS's system Bash.

## Guest and feature limits

The earlier Apple silicon checks used disposable copies of private Windows 95
media. Windows reached a clean 640 x 480, 256-color desktop, and the ScanDisk
Exit/Enter sequence and clean Windows shutdown worked. The complete evidence
and limits are recorded in [Mac emulation](MACOS-EMULATION.md).

Windows 95 remains experimental. A VMM exception during rapid Display Properties
tab switching and a DOS text-layout artifact remain unresolved. No long-session,
full guest-application, physical-speaker or Intel Windows 95 validation is claimed.
The bundled open-source demo is the guest used in release CI.

ZIP import, 4 GiB raw-disk boundaries, font import, custom shells and five-board
3D projection checks are described in [feature QA](QA-DESKTOP-MEDIA-PCB.md) and
[font QA](QA-FONT-ROM.md). The console keyboard, TrackPoint, mouse buttons and
pen pad are now interactive; the desktop keyboard and pointer remain available.

October 12 retesting reached a clean Windows desktop using another disposable
copy of the original image. Pointer movement and a desktop right-click worked.
The original display driver's CHIPS page reported mode 30h, 640 x 480 and
256 colors. All Display Properties pages opened with paced input; guest startup
also produced non-silent PCM. The session ran for over 20 minutes and completed
the guest's normal shutdown. Rapid synthetic modifier-key sequences do not reliably
activate every requested tab and need further investigation.
The 100-tab synthetic burst is not a stability pass: it can exceed the engine's
keyboard queue and leave modifiers held. The earlier VMM failure is not resolved
by a successful boot or by an unreliable burst-input test.

## Source and checksums

The release includes per-architecture modified emulator source, dependency source
archives, rebuild instructions, input provenance, firmware source, and the
matching Java runtime sources and build metadata. The app retains its component
notices. The signed and stapled DMG bytes determine both `SHA256SUMS` and the
Homebrew cask hashes. Private debugging logs and guest media are excluded.
