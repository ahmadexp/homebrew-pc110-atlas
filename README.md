# PC110 Atlas downloads

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator. Import your own compatible BIOS
and raw disk images. IBM firmware and operating-system media are not included.

This repository hosts public releases, the Homebrew tap, package publishing
workflows, store assets, and the experimental IRIX source edition.

## Platform compatibility

PC110 Atlas brings the PC110 hardware reference and emulator to modern devices.
Availability checked September 14, 2026.

| Platform / channel | Compatibility | Download or installation | Availability |
| --- | --- | --- | --- |
| iPhone and iPad | iOS / iPadOS 17 or later | [App Store](https://apps.apple.com/us/app/pc-110/id6801404183) | Available |
| Mac App Store edition | macOS 14 or later, Apple M1 or later | [Mac App Store](https://apps.apple.com/us/app/pc-110/id6801404183) | Available |
| Apple Watch | watchOS 10 or later, paired iPhone | [App Store companion](https://apps.apple.com/us/app/pc-110/id6801404183) | Available; remote display and controls for the iPhone session |
| Apple Vision Pro | visionOS 2 or later | [App Store compatibility](https://apps.apple.com/us/app/pc-110/id6801404183) | Listed as compatible; see the store for the offered edition |
| Apple TV | tvOS 17 or later | No public download yet | Reference edition prepared; not listed in the current App Store release |
| Android | Android 8.0 or later, arm64 | [Google Play internal test](https://play.google.com/apps/internaltest/4701134158978166940) | Testing; invitation required |
| Ubuntu / Snap Store | amd64 and arm64 | [Snap Store](https://snapcraft.io/pc110-atlas) | Available on stable; `sudo snap install pc110-atlas` |
| Linux / APT | amd64 and arm64; tested on Ubuntu 24.04 | [Signed APT repository and setup](https://ahmadexp.github.io/homebrew-pc110-atlas/) | Available; DEB packages |
| Linux / YUM and DNF | x86_64 and aarch64; compatible RPM distributions | [Signed YUM/DNF repository and setup](https://ahmadexp.github.io/homebrew-pc110-atlas/) | Available; RPM packages |
| Windows installers | Windows 10 or later, x64 | [MSI](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-windows-x64.msi) or [EXE](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-windows-x64.exe) | Available |
| Windows / Chocolatey | Windows 10 or later, x64 | [NUPKG download](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas.1.0.0.nupkg) and [installation guide](https://github.com/ahmadexp/homebrew-pc110-atlas#install) | Tested package available; Community submission awaits review |
| Mac desktop / Homebrew | macOS 12 or later; Intel and Apple silicon | [Intel DMG](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-macos-x64.dmg), [Apple silicon DMG](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-macos-arm64.dmg), or Homebrew below | Available; Developer ID signed and Apple notarized |
| IRIX / Unix X11 | Experimental IRIX 6.5, MIPS n32 target | [IRIX source test kit](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/irix-v1.0.0) and [build instructions](https://github.com/ahmadexp/homebrew-pc110-atlas/blob/main/unix/README.md) | Source only; testing on SGI hardware is still required |

The Mac App Store and Homebrew packages are separate editions. Native Linux
packages require a distribution that satisfies their dependencies. The smaller
Unix edition requires a C99 compiler, GNU make, and X11 development libraries;
its frontend has been tested on Linux X11, but other Unix systems are unverified.

The Intel Mac and other portable desktop downloads use the portable PC110 core,
not QEMU, and do not include guest audio. The [Pinokio launcher](https://github.com/ahmadexp/pc110-atlas-pinokio)
selects the Intel DMG on Intel Macs and the separate Mac App Store edition on
Apple silicon. Import your own compatible media; guest compatibility varies.

[All desktop downloads and checksums](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.0)
include the portable desktop release, while the
[distribution validation record](https://github.com/ahmadexp/homebrew-pc110-atlas/blob/main/desktop/DISTRIBUTION_VALIDATION.md)
details what has been tested.

## Install

Ubuntu Snap Store:

```sh
sudo snap install pc110-atlas
```

APT and YUM/DNF installation instructions and the signing-key fingerprint
are available at [the package repository](https://ahmadexp.github.io/homebrew-pc110-atlas/).

Repository signing-key fingerprint:
`4B6FA5B0B9C8CC49F0C164C66D199F8D554224BC`.
The [public key](desktop/packaging/keys/pc110-atlas.asc) expires September 13, 2028.

Windows: download the MSI/EXE from Releases, or download the NUPKG and install
it from its directory with `choco install pc110-atlas --source . --version 1.0.0`.
The package downloads the public MSI and verifies its checksum. Once the
Chocolatey Community submission is accepted:

```powershell
choco install pc110-atlas
```

macOS 12 or later, Intel or Apple silicon:

```sh
brew tap ahmadexp/pc110-atlas
brew install --cask pc110-atlas
```

Alternatively, open the DMG matching your Mac and drag PC110 Atlas to Applications.
Do not replace a different edition already installed; keep both if needed.
The portable app has bundle ID `org.opensourcepc110.atlas.desktop`, separate from
the Mac App Store app. Leave Gatekeeper enabled. Compare the downloaded file's
`shasum -a 256` with the release's `SHA256SUMS`.

For IRIX, download the source testing kit from Releases and follow its
`START-HERE.txt`. It requires GCC with C99 support, GNU make, and the system
X11 development libraries. There is no precompiled IRIX binary yet.

Matching Java runtime sources and build inputs are attached to each desktop
release. See [runtime source details](desktop/packaging/RUNTIME-SOURCES.md).

## Documentation and support

- [Desktop usage](desktop/README.md)
- [IRIX build and testing](unix/README.md)
- [Publishing guide](desktop/DISTRIBUTION.md)
- [License scope and third-party terms](LICENSING.md)
- [Privacy](PRIVACY.md)
- [Report an issue](https://github.com/ahmadexp/homebrew-pc110-atlas/issues)

The original application code is MIT licensed. Hardware material retains
its existing terms. This is an independent project and is not affiliated
with or endorsed by IBM.
