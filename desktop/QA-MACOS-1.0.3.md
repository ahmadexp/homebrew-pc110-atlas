# Mac 1.0.3 release validation

Final installers verified October 17, 2026, on their native architectures.

## Build scope

- Application source inputs: `6ed13da`; subsequent changes are documentation only.
- Local native builds for Intel and Apple silicon with a macOS 12 deployment
  baseline. Tests run on newer installed macOS versions, not every supported OS.
- Eclipse Temurin 21.0.12.1+1-LTS, with its matching source and build attachments.
- 50 desktop JVM/native tests and 41 packaging tests pass on both architectures.
- Fresh exports of the iPhone keyboard match all 90 key regions and 2,880
  key/modifier combinations on both Macs. Focused tests cover Up's center,
  boundaries and neighbors, and matching pictured/physical press and release.
- The pictured Up key produced guest BIOS code `4800` in the signed Apple
  silicon app. The maintainer confirmed the same physical Up-key result.
- No hosted build runners, signing-key exports or proprietary guest-media
  uploads are used for this release.

## Installer verification

Both installers are Developer ID signed, Apple notarized and stapled.
Their exact final bytes passed native checks on October 17: DMG/app
signatures, Gatekeeper, stapling, architecture and version, all 19 schematic
page renders, packaged native loading, private media copying and runtime startup.

The Intel runtime built locally and passed text output, 256-color graphics,
keyboard input and non-silent stereo PCM transport. Its final signed and stapled
installer was transferred back to the Intel Mac and passed the same packaged
checks. The locally computed checksum matches the Intel verification result.

The packaged guest smoke suite covers reset, clean process stop, fresh-process
restart, Unicode/comma paths and preservation of read-only demo media. The pipe
handshake verifies the direct-pointer protocol and bridge versions. The demo
does not establish complete PersonaWare or Windows driver compatibility.

Verified final DMG SHA-256 values:

- Apple silicon: `1a7bbe5d4a9dbd66f926d812f2afcb77f2d04d657f13d9bd0dd3c8c375941bd2`
- Intel: `065852b5a51d55e19aee2c64fb57a7f5ec56e9eb6431610dfd064981d390b839`

## Limits

Prior [media, PCB and guest checks](QA-MACOS-1.0.2.md) remain relevant, but are
not represented as newly repeated physical-device tests. Windows 95 remains
experimental. The intermittent VMM exception and historical DOS text artifact
are not declared fixed. There is no new claim of full guest-application,
long-session, physical-speaker or Intel Windows 95 validation.

Release uploads must contain only the verified installers, checksums,
documentation and required source/license attachments. Private build logs,
account details, credentials, personal disks and screenshots are excluded.
