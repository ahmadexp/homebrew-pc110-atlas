# PC110 Atlas 1.0.1, Pi-Apps submission

Submitted September 18, 2026: [Pi-Apps PR #3051](https://github.com/Botspot/pi-apps/pull/3051).
The ARM64 review release is published. All five public-artifact integration
jobs and all six selected upstream ARM64 OS-image jobs passed for the identical
installer tree. ShellCheck also passed. Final metadata-only commit image checks
are running. The PR is open for maintainer review, not yet accepted into the catalog.

The two automatic upstream PR checks stopped at checkout, before app validation:
[Check PR](https://github.com/Botspot/pi-apps/actions/runs/35410297399) and
[Shellcheck](https://github.com/Botspot/pi-apps/actions/runs/35410297404).
GitHub refuses to check out fork code in their privileged `pull_request_target`
context. This needs upstream maintainer attention; no security override or
upstream workflow change is part of this submission. The passing fork and
public-artifact results below are unaffected.

## App and release

Release URLs below are public downloads. Existing 1.0.0 channels are unchanged.

PC110 Atlas is an interactive hardware reference, historical archive and PC110
emulator. Explore PCB layers and offline schematics without firmware, try the
original bundled boot demo, or import legally supplied BIOS/disk images.
No IBM ROMs, Windows, DOS or PersonaWare are distributed.

- [Project/support](https://github.com/ahmadexp/homebrew-pc110-atlas)
- [Linux ARM64 review release](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.1)
- [Import ZIP](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.1/PC110-Atlas-Pi-Apps-1.0.1.zip)
- ZIP SHA-256: `c2dbf46f62e4d4a22fdbabb224a5f7381c37235da3b93ad86c0dc7853db61272`
- DEB SHA-256: `2890c907e7087532ff860c6aada02017913305e8701a13791936e8f80c053f5b`

Exact modified QEMU source/build inputs, SeaBIOS notices/source and
matching Temurin source/build scripts accompany the release. Original code is
MIT; hardware material is CC BY-NC 4.0; dependencies retain their own terms.
See LICENSING.md. The project is independent of IBM.

## Installer

Seven-file ARM64 script-app. SHA-256-checked HTTPS download followed by
`install_packages`; `purge_packages` on uninstall preserves media/preferences.
No external APT repository is added. Java is bundled. Proposed category:
`Tools/Emulation`. The installed desktop shortcut is in Education.

## Evidence and limits

- One DEB built on native Ubuntu 22.04 ARM64 passed clean-container install,
  native/QEMU smoke, four UI renders, reinstall, purge and media preservation on
  Bookworm, Trixie, Jammy, Noble and Resolute.
- Packaged smoke passed on a real 4 GB Pi 5 running Raspberry Pi OS Trixie.
- Interactive source-equivalent Pi 5 tests covered media import, PCB layout,
  window resizing and offline PDF viewing. Original/English PersonaWare copies
  booted and calculated 2 + 3 = 5. Mouse clicks opened WorldClock.
- 23 desktop tests and 29 packaging tests passed. QEMU GLIBC requirements are
  checked at packaging time, preventing accidental use of a newer baseline.
- Physical speaker output, Windows 95, other Pi models and every guest
  application are not certified. No private media/screenshots are submitted.
- 32-bit ARM and older unsupported distributions are rejected before download.
  Pi-Apps permits ARM64-only apps.

See [hardware/compatibility report](HARDWARE-TEST.md). The PR records the exact
tested systems and limits; it does not claim physical desktop testing on every
system. The all-systems issue-template confirmation must never be used to hide
untested platforms.

## GitHub-hosted checks

- [ShellCheck](https://github.com/ahmadexp/pi-apps/actions/runs/35410316209): passed.
- [Public-artifact integration](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/35289524731): passed on all five distributions. QEMU boot, graphics, keyboard, PCM transport, reset/restart and read-only media checks passed. Four UI exports, reinstall, repeated uninstall and preservation of both default/custom media directories also passed. The CI-rebuilt import ZIP exactly matches the published ZIP checksum.
- [Upstream OS-image install/uninstall](https://github.com/ahmadexp/pi-apps/actions/runs/35410295929): final metadata-only commit verification is running on Bookworm, Trixie, Pi Ubuntu Noble/Resolute and Switchroot Jammy/Noble, all ARM64. The identical installer tree already passed all six jobs on September 18. Bullseye and 32-bit jobs are intentionally disabled.

Submission branch: `ahmadexp:pc110-atlas-1.0.1`, commit `7c1c793`.
Only the seven app files and one `Tools/Emulation` category entry are proposed
upstream. The distribution repository carries the release documentation and
additional reproducible helper tests. Other release channels remain unchanged.
