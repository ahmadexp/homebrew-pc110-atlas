# Distribution validation, September 14, 2026

Version 1.0.0 is available from the
[public release](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.0).
The [signed package repositories](https://ahmadexp.github.io/homebrew-pc110-atlas/)
are deployed and have passed checks against their public HTTPS URLs.

| Check | Result |
| --- | --- |
| Native macOS arm64 and x64 DMG builds and packaged launcher smoke tests | Passed in native CI |
| Both macOS candidates signed with Developer ID, signature verification and signed launcher tests | Passed locally, with x64 execution through Rosetta on Apple silicon |
| Apple notarization and stapling | Pending notarization credentials; Mac downloads and Homebrew cask are not published |
| Windows x64 MSI/EXE builds, MSI installation and launcher smoke test | Passed in native Windows CI |
| Chocolatey NUPKG from public MSI: pack, install, launch and uninstall | [Passed](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34864274829) |
| Linux arm64 and x64 DEB/RPM builds and desktop tests | Passed on native Ubuntu 24.04 runners |
| Both architectures: APT package installation and installed launcher tests | Passed |
| Both architectures: Fedora DNF package installation and launcher tests | Passed |
| Both architectures: strict Snap build, installation and confined launcher tests | Passed |
| Public APT key fingerprint, signed metadata, APT update and package candidate | [Passed after deployment](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34865017831) |
| Public RPM repository metadata signatures for x86_64 and aarch64 | Passed after deployment |
| APT metadata, architecture indexes, signed RPM packages and tamper rejection | Passed integration checks with disposable packages and a temporary key |
| Release manifest and checksum unit tests | 6 passed |
| GitHub Actions workflow validation with actionlint | Passed |
| Unix frontend build and X11 tests on Linux x86_64 at 8-, 16-, and 24-bit depth | Passed |
| Portable core synthetic BIOS boot on emulated big-endian MIPS Linux | Passed |
| IRIX source test kit public download and checksum verification | Passed |
| Actual IRIX 6.5 / SGI workstation execution | Pending hardware testing; no precompiled IRIX executable is claimed |
| Snap Store listing and submission | Name registered and agreement accepted; listing and upload pending |
| Chocolatey Community submission | Pending publishing API key |

The portable desktop edition bundles Eclipse Temurin 21.0.12.1+1-LTS. Its
matching sources and build inputs are attached to the public release, together
with license notices, `BUILD-PROVENANCE.json` and `SHA256SUMS`. Original code is
MIT licensed; hardware material and third-party libraries retain their terms.

Public package provenance:

- Windows and Mac candidates: source commit `967f2fc146a92d6da3d736f75e3f240b4c82da3e`, build `34862491797`.
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
