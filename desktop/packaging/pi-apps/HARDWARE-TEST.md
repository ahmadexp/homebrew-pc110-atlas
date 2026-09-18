# Raspberry Pi hardware test, September 17, 2026

Latest result: the Linux QEMU 1.0.1 fix candidate resolves the reproduced
picker, PCB layout, resize and PersonaWare execution failures on this Pi 5.
The new offline PDF viewer was also inspected successfully. See the dated fix
retest below. A subsequent Ubuntu 22.04-baseline build also passes native ARM64
container checks on Bookworm, Trixie, Jammy, Noble and Resolute and packaged
smoke tests on the Pi. This is not Pi-Apps acceptance or broad hardware sign-off.

Original 1.0.0 result: partial pass. Installation and a
synthetic guest boot passed, but the default media picker failed. The PCB-layer
dialog also opened too small to display its content. The host became unreachable
during the initial PDF-viewer check. Access was later restored; private-media
testing then exposed a portable-core execution failure, described below.

## System and package

- Raspberry Pi 5 Model B Rev 1.0, 4 GB RAM, ARM64.
- 64-bit Raspberry Pi OS Trixie, Debian 13.6; reference image dated 2025-11-24.
- labwc Wayland desktop, Xwayland `:0`, 1920 x 1080 display at scale 1.
- Broadcom V3D 7.1.7.0; Mesa `26.2.0-1~bpo13+0~rpt3`; `glxinfo -B`
  reported direct rendering and acceleration. This does not establish that
  every app rendering path works correctly.
- Unchanged public ARM64 desktop DEB 1.0.0, SHA-256
  `0e13ea75ed6d2c908a461a2944f4b5be3ae23f2f4b056090565c4bb43d128014`.
- Candidate ZIP SHA-256
  `7429d413e8911668027c75b6d0dde3d06a403a98f228bafa5df82c48d280f6cf`.
- Pi-Apps checkout `9cb5e7d21b4ec38421fd241856d1a7e106e546c0`.

The Pi-Apps checkout was staged in a dedicated QA directory. Its real
`manage install 'PC110 Atlas'` command installed the candidate; the Pi-Apps
desktop application itself was not installed as a normal system service/menu
entry. No OS upgrade or repository changes were made.

## Observations

| Check | Result |
| --- | --- |
| Real Pi-Apps installation | Passed; `pc110-atlas` 1.0.0 ARM64 and helper package installed |
| Packaged `--smoke-test` | Passed, including native core loading |
| Packaged four-screen export | Passed on the Pi; separate from interactive desktop checks |
| Discover, Run, Hardware navigation and scrolling | Passed |
| Board reference image and component selection | Passed; selection changed from 486SX to SCAMP IV |
| Default native media picker | Failed, black GTK chooser with FreeType drawing errors |
| Native picker with system FreeType preloaded | Rendered correctly; BIOS and raw disk imports passed, copied hashes matched |
| Synthetic guest boot, keyboard input, reset and power off | Passed with the FreeType launch workaround |
| PCB-layer dialog | Failed layout check; opened at 390 x 270 with no usable board preview |
| Resize | Not validated; synthetic X11 resize enlarged the outer window without relayout, including with software rendering |
| PDF schematic | Viewer process launched, but the host stopped responding before its contents could be inspected |
| Relaunch and media persistence | Relaunch found the isolated test media; normal production preferences were not changed |
| Real-device reinstall/uninstall | Not run; container results remain the only evidence for those operations |

The synthetic guest used an original 64 KiB BIOS and a 512-byte raw boot
sector, not IBM firmware or an operating system. The BIOS loaded the sector
through the portable core's disk service, and the sector printed a test banner
and echoed `Pi 5 keyboard test 123` through the guest keyboard path. An initial
fixture used drive 80h incorrectly; the final fixture uses drive 00h, matching
the core's presentation of this partitionless image. No application code was
changed to make the guest pass. This test does not establish Windows 95 or
PersonaWare compatibility, graphics-mode coverage, guest pointer support, or
guest audio support.

## Native picker diagnosis

The default launcher produced repeated GTK messages:

```text
drawing failure for widget 'GtkFileChooserDialog': error occurred in libfreetype
```

The process mapped both the bundled JRE's FreeType library and the system
FreeType library. A process-local diagnostic launch with
`LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libfreetype.so.6` made the same chooser
render and import files successfully. System FreeType was
`2.13.3+dfsg-1+deb13u1`; GTK was `1:3.24.49-3+rpt8`.

This A/B result points to a native library interaction. It is a diagnostic
workaround, not a shipped fix or a verified solution for every supported OS.
No installed application file, system library, global environment variable, or
desktop shortcut was modified. Software rendering was also tried separately
in combination with the preload; it did not resolve the observed resize issue.
The last launch used that combined diagnostic configuration.

## Host interruption and safety

The Pi desktop displayed a low-voltage warning before the PDF check.
`vcgencmd get_throttled` returned `0x50000` and temperature was 51 C. No
performance or stability benchmark is claimed. After opening the Mainboard
schematic, an Evince process appeared in the app log, then SSH and ping stopped
responding. The cause is not established. Check power and connectivity before
retesting the viewer or drawing any causal conclusion.

In the initial synthetic test, all imported files were original disposable fixtures in a dedicated QA
`XDG_DATA_HOME`; Java preferences were isolated too. No personal ROMs, disk
images, or existing media were copied or changed. The app remains installed;
its last running state could not be confirmed after connectivity was lost.

Diagnostic packages installed were `jq`, `libjq1`, `libonig5`, `yad`,
`xdotool`, `libxdo3`, `mesa-utils`, and `mesa-utils-bin`. Existing packages were
not upgraded. Real-device uninstall was intentionally skipped: the Pi already
had unrelated auto-removable packages, and upstream's helper invokes APT with
autoremove. Do not remove those packages as part of app testing. Installation
and test staging were left in place for follow-up.

Local evidence is under `build/pi-apps-20260917/`, including
`installation.log`, `file-chooser.png`, `freetype-chooser-full.png`,
`guest-input-focused.png`, `maximize-reset.png`, `live-hardware.png`,
`live-schematic-menu.png`, the original fixture assembly, and launch scripts.
Some detailed runtime logs remain on the Pi until it reconnects. Do not present
an unfinished screenshot command as a successful PDF capture.

## Original gates, before the fix retest

1. Inspect the earlier host interruption and recheck its power supply without
   assuming the PDF viewer caused it. Access has been restored, but PDF rendering
   and stability remain unverified.
2. Fix and regression-test the normal launcher/media picker and PCB-layer
   dialog in a new candidate. Do not replace a published artifact in place.
3. Validate ordinary window resizing, PDF rendering, remaining reference views,
   and representative legally supplied guests with keyboard/pointer input.
4. Test safe reinstall/uninstall on a disposable Pi installation, then complete
   upstream supported-image tests and resolve the minimum-OS acceptance limit.
5. Only then update the submission checklist. No issue, PR, or public Pi-Apps
   listing was submitted in this test.

## Follow-up with user-supplied media

After a host reboot, access was restored and throttling flags were `0x0`.
At the user's request, private copies of their BIOS, font ROM, controller
firmware, and PersonaWare disk images were loaded in a separate, access-limited
test directory. Original media and production preferences were preserved;
checksums matched before and after testing. No personal media or screenshots
are included in the candidate or this public evidence record.

The original PersonaWare image reached its graphical menu and the pointer
moved, but applications did not open through clicks or keyboard navigation.
The English alternative remained at `Starting PC DOS...` during the observed
roughly 87-second interval. A separate diagnostic using the unchanged installed
native library confirmed firmware loading and reproduced a stopped CPU at
linear PC `0000BB08`, including in a no-input baseline. Its instruction counter
did not advance between samples. This is not a usable PersonaWare pass.

Source inspection also found that the desktop's primary mouse button uses 1
while the portable core expects 0. Correcting that mismatch alone is not yet
shown to resolve the independent CPU stop. Core execution and input fixes need
regression tests before any full guest compatibility claim. The diagnostic
scripts, logs, and guest captures are private local artifacts, not release assets.

## Linux QEMU fix retest, September 17, 2026

The same Pi 5 and Raspberry Pi OS desktop were used. A private 1.0.1 ARM64 DEB
was built on native Ubuntu 24.04 ARM64 with the pinned Temurin 21 runtime and
tested side by side with the installed public 1.0.0 package. No published file,
Pi-Apps installer pin, production preference, or original personal media was
replaced. This candidate bundles the shared PC110 QEMU backend instead of using
the portable CPU for guest execution. The portable CPU stop itself is not fixed.

| Retest | Result |
| --- | --- |
| Media picker without FreeType preload | Passed; Swing chooser displayed, BIOS reimported and copied checksum matched |
| PCB layers | Passed; large initial dialog, spacing control visible and usable, 640 x 480 resize retained preview and controls |
| Main window resize/maximize/fullscreen | Passed after the process-local Wayland environment initialization; no desktop configuration changes |
| Mainboard PDF | Passed in the built-in viewer, including 100%, 300% and page 2; no external PDF application used |
| Original PersonaWare image | Boot, four-corner pen calibration, menu, keyboard navigation and Calculator passed; 2 + 3 = 5 in the direct QEMU test |
| English PersonaWare alternative | Boot, calibration, menu and Calculator passed; 2 + 3 = 5 in the direct QEMU test |
| Actual desktop guest pointer | Passed; mouse movement and primary click opened WorldClock, keyboard navigation opened Calculator |
| QEMU packaged integration smoke | Passed on Pi: text, graphics, keyboard, PCM audio transport, reset, stop/restart, Unicode paths and read-only demo |
| Packaged native-core smoke | Passed on Pi and disposable ARM64 Linux containers |
| Source regression tests | 23 desktop tests passed on Mac ARM64 and Linux ARM64; 28 packaging tests passed |
| Candidate APT lifecycle | Earlier private revision passed fresh Trixie install, reinstall, purge and synthetic-media preservation; not a real-Pi uninstall test |

The English guest reports pre-existing DOS driver/COUNTRY configuration warnings
but proceeds to a usable menu and Calculator. This does not establish that every
application in either image works. The Modern image, Windows 95, physical audio
output, Pi 4, Linux x86-64 QEMU packages and RPM lifecycle were not validated in
this retest. PCM transport passing is not evidence of sound from the Pi speakers.

The black native chooser is avoided by selecting Swing on Linux. The window
resize failure reproduced in SSH launches without labwc's usual Java flag.
Before AWT initializes, the app now sets `_JAVA_AWT_WM_NONREPARENTING=1` only
when running under Wayland and no value already exists. Final UI tests removed
all external FreeType, Skiko and Java window-manager workarounds. The earlier
host interruption remains unexplained; the repeat PDF checks stayed reachable
and reported no current throttling. No claim of a repaired power supply is made.

Private revision 3 also forwards numeric-keypad add, subtract, multiply and
Enter, and explicitly declares libffi8 and GLIBC 2.38 dependencies. The DEB
SHA-256 is `054cbf36a971866d099a44eed69d60dc1ae469d07132e4f4ab1af3b9c82c78b8`.
Its packaged native-core/QEMU smoke tests passed both on the actual Pi and
after APT reinstall in the Ubuntu Noble ARM64 build container. In the actual
revision 3 desktop UI, PersonaWare booted again, completed calibration and
computed 2 + 3 = 5 with the numeric-keypad add key. It is left open for local
review with mouse input selected. All seven original personal-media checksums
were verified unchanged. A transfer attempt was extracted before completion;
that incomplete extraction was retained separately, and the final package was
re-extracted only after its SHA-256 matched the build output.
Earlier private revision 2, used for the listed layout/PDF checks, had SHA-256
`134a177ef36a67da13c483c3b3308871e2fc19a8db3751404170c1d0e7737958`.
These are local candidates, not publicly downloadable releases.

Diagnostic `wtype` was added to operate labwc window shortcuts. No existing Pi
packages were upgraded. Private test images were copied into an isolated media
directory before boot; changes made by the guest affect only those copies.
The installed 1.0.0 package remains in place. Private guest screenshots are not
release or store assets.

Local evidence remains under `build/pi-apps-20260917/`: the `fix-*` build/test
logs, `fixed-r2-layers-minimum.png`, `fixed-r2-max.png`, `fixed-picker-ready.png`,
`fixed-pdf-zoom.png`, `fix-pi-r3-bundled-qemu.log`,
`fix-r3-noble-installed.log`, and private QEMU guest captures including
`fixed-r3-keypad-calculation.png`. The native ARM64 build and
DEB are staged under `build/pi-fix-candidate-20260917/`.

### Remaining release gates

1. Publish a new immutable release only after reviewing the final candidate.
   Repoint the Pi-Apps checksum/URL and regenerate its ZIP together; never
   overwrite the public 1.0.0 artifact.
2. Re-run the actual Pi-Apps helper workflow against that final public artifact,
   including safe lifecycle tests on a disposable Pi image.
3. Run and link upstream supported-image tests, and obtain agreement on the
   Trixie/Noble minimum OS. Bookworm/Jammy and 32-bit ARM remain unsupported.
4. Recheck submission requirements and duplicates. No issue, PR or public
   Pi-Apps listing has been submitted by this fix retest.

## Older-baseline compatibility retest, September 17, 2026

The Trixie/Noble-only dependency limit is superseded for the new candidate.
QEMU and the JNI library were rebuilt on native Ubuntu 22.04 ARM64 using the
same pinned Temurin JDK. QEMU now requires at most GLIBC 2.34 symbols, and the
package declares the conservative Ubuntu 22.04 baseline, GLIBC 2.35. Release
packaging rejects QEMU executables requiring newer symbols. Library dependencies
work with both original and t64 package names; no mixed repositories or forced
dependencies are used.

Final candidate DEB SHA-256:
`2890c907e7087532ff860c6aada02017913305e8701a13791936e8f80c053f5b`.
Pi-Apps ZIP SHA-256:
`c2dbf46f62e4d4a22fdbabb224a5f7381c37235da3b93ad86c0dc7853db61272`.
The previously staged Trixie-only candidate is superseded, not published.

| Native ARM64 container | Same final DEB: install, native/QEMU smoke, four UI exports, reinstall, purge, media preservation |
| --- | --- |
| Debian Bookworm | Passed |
| Debian Trixie | Passed |
| Ubuntu 22.04 Jammy | Passed |
| Ubuntu 24.04 Noble | Passed |
| Ubuntu 26.04 Resolute | Passed |

The final candidate also passed native-core and full packaged QEMU smoke on the
real Pi 5, including graphics, keyboard, PCM transport, reset/restart, Unicode
paths and read-only demo media. It was extracted side by side, leaving installed
1.0.0, the earlier interactive session and original personal media untouched.
The interactive GUI/PersonaWare evidence above used the same app/guest-device
code before rebuilding against older system libraries. No new physical audio,
other-Pi-model or Switchroot/Jetson desktop claim follows from these tests.

23 desktop tests passed on Jammy ARM64; all 29 packaging tests, ShellCheck and
actionlint passed. The first container test attempt precreated the QEMU evidence
directory and was correctly rejected by the smoke test's overwrite guard.
The corrected harness used fresh directories; no application change was needed.
Logs and screenshots are local under `build/pi-compat-20260917.t9vepz/`, with
passing lifecycle logs named `*-integration-v2.log` and Pi smoke evidence in
`pi-package-smoke.log`. This is not the upstream OS-image workflow.

At this checkpoint no release, PR or issue has been published. A new immutable
1.0.1 release, public-artifact helper checks and upstream OS-image checks are
still required. GitHub Actions is initially disabled on the submission fork;
permission to enable the required checks has been requested. ARM64-only is
permitted by the current Pi-Apps contribution guidance. Bullseye, older systems
and 32-bit ARM remain unsupported. No minimum-OS exception for Bookworm/Jammy
is needed for this rebuilt candidate.
