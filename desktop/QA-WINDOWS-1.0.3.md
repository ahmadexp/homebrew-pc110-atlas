# Windows 1.0.3 release validation

Verified October 17, 2026 on a local Windows 11 Pro x64 machine. No hosted
build runners were used.

## Build and tests

- Application source inputs: `6ed13da`, matching the Mac 1.0.3 release.
- Isolated Temurin 21.0.12.1+1, MSYS2 UCRT64 and WiX 3.14.1 build tools;
  Visual Studio 2022 compiles the desktop native library.
- All 50 desktop JVM/native tests passed with no failures or skips.
- Packaging suite: 41 discovered, 23 passed and 18 platform-specific skips.
- The keyboard fixture matches the fresh Swift exports checked on both Macs:
  90 key regions and 2,880 key/modifier combinations. Windows regression tests
  cover Up's position, neighbors and pictured/physical key codes.
- Native transport checks passed for boot text, 256-color graphics, keyboard,
  non-silent stereo PCM, direct-pointer protocol 2 and bridge ABI 4.
- The bundled runtime includes its exact modified source, dependency sources,
  component licenses and checksums. Dependency source downloads were verified
  over TLS on the Mac and checked against the Windows package versions and
  archive hashes before packaging.

## Final installers

Both MSI and EXE passed separate clean installation and removal tests. Each
installed launcher passed all 19 schematic-page renders, native library loading,
graphics initialization, private media import and runtime startup. The packaged
guest tests passed text, 256-color graphics, keyboard, non-silent PCM transport,
reset, stop/restart, Unicode/comma paths and preservation of read-only demo media.

SHA-256:

- MSI: `178c3f354242eff2c8c262e8353203a744db12cf80e0d6c911c854dba4c6f23c`
- EXE: `b07270262848f9d64dfe4b770ed411fedc420b49d1bee19a7095b8b571abb0e0`

These Windows installers are not Authenticode signed. Windows may show an
unknown-publisher warning. The Mac installers are signed and notarized separately.

## Chocolatey package

The 1.0.3 NUPKG passed a complete local Chocolatey install/uninstall cycle.
It downloaded the public GitHub MSI, verified the pinned SHA-256, installed
successfully, and passed the installed launcher and guest runtime smoke suites.
Automatic uninstallation then removed the test installation. No existing user
installation or personal media was removed.

NUPKG SHA-256:
`78c71d395716f7ed46de715cc2cd0fd6f53190dd2525f89bf2a037057b2f14e9`.
The Community Repository accepted the upload on October 17. Its package page
shows validation, verification and scanning pending. Local validation does
not mean the Community Repository has approved the update; moderation is
still pending.

## Limits

The target is Windows 10 or later, x64; this release was tested on Windows 11,
not every supported Windows version. Automated key-code tests do not replace
an interactive physical-keyboard check on every host. Audio transport tests
do not establish physical-speaker output quality.

Windows 95 remains experimental. Known guest stability and text-layout issues
are not declared fixed. Direct pointing requires a compatible guest driver;
recognized FAT12/FAT16 working disks receive automatic preparation with a
recoverable backup, while unsupported formats retain relative input. This
demo-based validation is not a complete PersonaWare or Windows 95 session test.

No proprietary firmware, operating systems, personal media, account details or
private build logs are included in the public release.
