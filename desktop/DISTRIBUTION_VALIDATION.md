# Distribution validation, September 15, 2026

Version 1.0.0 is available from the
[public release](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.0).
The [signed package repositories](https://ahmadexp.github.io/homebrew-pc110-atlas/)
are deployed and have passed checks against their public HTTPS URLs.

| Check | Result |
| --- | --- |
| Native macOS arm64 and x64 DMG builds and packaged launcher smoke tests | Passed in native CI |
| Both macOS candidates signed with Developer ID, signature verification and signed launcher tests | Passed locally, with x64 execution through Rosetta on Apple silicon |
| Apple notarization and stapling | Both Mac DMGs accepted, tickets stapled and validated; Gatekeeper accepted the notarized Developer ID |
| Mac minimum OS target | PC110 JNI core rebuilt from matching release sources for macOS 12.0; packaged binaries inspected |
| Final Mac packaged launcher smoke tests | Passed on Apple silicon, including x64 through Rosetta; actual execution on macOS 12 remains unverified |
| Pinokio launcher contracts | 24 passed on Intel Mac, Apple silicon, Windows, Linux x64 and Linux ARM64 in [CI](https://github.com/ahmadexp/pc110-atlas-pinokio/actions/runs/34926993475); Intel Mac Pinokio GUI installation remains unverified |
| Windows x64 MSI/EXE builds, MSI installation and launcher smoke test | Passed in native Windows CI |
| Corrected Chocolatey 1.0.0 NUPKG from unchanged public MSI: pack, install, launch and uninstall | [Passed](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34980697863) |
| Linux arm64 and x64 DEB/RPM builds and desktop tests | Passed on native Ubuntu 24.04 runners |
| Both architectures: APT package installation and installed launcher tests | Passed |
| Both architectures: Fedora DNF package installation and launcher tests | Passed |
| Both architectures: strict Snap build, installation and confined launcher tests | Passed |
| Public APT key fingerprint, signed metadata, APT update and package candidate | [Passed after deployment](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34865017831) |
| Public RPM repository metadata signatures for x86_64 and aarch64 | Passed after deployment |
| APT metadata, architecture indexes, signed RPM packages and tamper rejection | Passed integration checks with disposable packages and a temporary key |
| Release manifest, checksum and archived native signing unit tests | 14 passed; includes release-pinned CDN icon and same-version checksum replacement coverage |
| GitHub Actions workflow validation with actionlint | Passed |
| Unix frontend build and X11 tests on Linux x86_64 at 8-, 16-, and 24-bit depth | Passed |
| Portable core synthetic BIOS boot on emulated big-endian MIPS Linux | Passed |
| IRIX source test kit public download and checksum verification | Passed |
| Actual IRIX 6.5 / SGI workstation execution | Pending hardware testing; no precompiled IRIX executable is claimed |
| Snap Store uploads and stable release, amd64 revision 1 and arm64 revision 2 | [Published](https://snapcraft.io/pc110-atlas), [upload workflow passed](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34867075816) |
| Store download on Ubuntu arm64, edge launch, stable refresh and launch | Passed with strict confinement |
| Public listing title, description, category, license, links, icon and four Ubuntu screenshots | Saved and visually verified |
| Original Chocolatey Community automated validation, verification and virus scan | All passed before human review |
| Chocolatey icon URL moderation correction | jsDelivr PNG verified against the release icon, pinned to `desktop-v1.0.0`; only `iconUrl` changed in package metadata, installation script unchanged |
| Chocolatey Community 1.0.0 resubmission | [Upload succeeded](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34980975480); response posted in [review comments](https://community.chocolatey.org/packages/pc110-atlas/1.0.0); renewed automated checks and reviewer approval pending |

The portable desktop edition bundles Eclipse Temurin 21.0.12.1+1-LTS. Its
matching sources and build inputs are attached to the public release, together
with license notices, `BUILD-PROVENANCE.json` and `SHA256SUMS`. Original code is
MIT licensed; hardware material and third-party libraries retain their terms.

Public package provenance:

- Windows and Mac candidates: source commit `967f2fc146a92d6da3d736f75e3f240b4c82da3e`, build `34862491797`.
- Corrected Chocolatey NUPKG: packaging commit `58f6670680edff326bf0f8800601c10756ee2550`, build `34980697863`; SHA-256 `3d3d20c75b0859ab54ce9165a3bbb90e0b59ca7c9b7caf740665d7800c69c0c2`. Windows installer bytes and every other release asset checksum are unchanged.
- Final Mac DMGs retain that application's Java code and runtime. Their matching PC110 JNI sources were rebuilt with deployment target 12.0; archived native libraries, app bundles and DMGs were Developer ID signed before notarization. The first attempt exposed unsigned JAR-contained libraries; the final candidates correct those signatures and the minimum OS target. See the release's `BUILD-PROVENANCE.json` for final notarization IDs.
- Linux packages with the pinned runtime: source commit `83f54c4faa7c124f91df5ab44e0022c11757a66f`, build `34864108656`.
- Snap packages with the pinned runtime: source commit `4efc1a0eb0e7326ac599b7e10df8ca9830edf167`, successful Snap jobs in build `34863723925`. Linux jobs in that earlier run failed at Java setup and were replaced by the successful Linux build above.

Four 1600 x 1000 Ubuntu screenshots in `snap/screenshots/` were exported from
the installed native Linux launcher and visually checked. The same screens
are included in the store submission asset bundle. Screenshots show the
portable edition without imported proprietary firmware or operating systems.

The tests verify packaging, native library loading, image decoding and
disposable media import. They do not establish compatibility with every guest
operating system or older Linux distribution. Actual SGI/IRIX execution remains
an explicit experimental target.
