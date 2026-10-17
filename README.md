# PC110 Atlas downloads

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator. Import your own compatible BIOS
and raw disk images. IBM firmware and operating-system media are not included.

This repository hosts public releases, the Homebrew tap, package publishing
workflows, store assets, and the experimental IRIX source edition.

## Platform compatibility

PC110 Atlas brings the PC110 hardware reference and emulator to modern devices.
Mac/Homebrew availability updated October 17, 2026, and Chocolatey approval
verified October 16. Other rows retain their
previously recorded channel status; this Mac update does not republish them.

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
| Raspberry Pi / Pi-Apps | ARM64 for Bookworm/Trixie and Ubuntu Jammy/Noble/Resolute | [1.0.1 review build and testing guide](desktop/packaging/pi-apps/README.md) | [Submitted in PR #3051](https://github.com/Botspot/pi-apps/pull/3051); five-distribution integration and six ARM64 OS-image checks passed, maintainer approval pending |
| Linux / YUM and DNF | x86_64 and aarch64; compatible RPM distributions | [Signed YUM/DNF repository and setup](https://ahmadexp.github.io/homebrew-pc110-atlas/) | Available; RPM packages |
| Windows installers | Windows 10 or later, x64 | [MSI](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-windows-x64.msi) or [EXE](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.0/pc110-atlas-1.0.0-windows-x64.exe) | Available |
| Windows / Chocolatey | Windows 10 or later, x64 | [Chocolatey package](https://community.chocolatey.org/packages/pc110-atlas/1.0.0) and [installation guide](https://github.com/ahmadexp/homebrew-pc110-atlas#install) | 1.0.0 approved September 23, 2026; verified October 16 |
| Mac desktop / Homebrew | macOS 12 or later; Intel and Apple silicon | [Intel DMG](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.3/pc110-atlas-1.0.3-macos-x64.dmg), [Apple silicon DMG](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/download/desktop-v1.0.3/pc110-atlas-1.0.3-macos-arm64.dmg), or Homebrew below | 1.0.3; direct screen pointing and corrected Up key; Developer ID signed and Apple notarized; Windows 95 experimental |
| IRIX / Unix X11 | Experimental IRIX 6.5, MIPS n32 target | [IRIX source test kit](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/irix-v1.0.0) and [build instructions](https://github.com/ahmadexp/homebrew-pc110-atlas/blob/main/unix/README.md) | Source only; testing on SGI hardware is still required |

The Mac App Store and Homebrew packages are separate editions. Native Linux
packages require a distribution that satisfies their dependencies. The smaller
Unix edition requires a C99 compiler, GNU make, and X11 development libraries;
its frontend has been tested on Linux X11, but other Unix systems are unverified.

Mac/Homebrew 1.0.3 adds direct screen pointing and the latest iPhone keyboard
layout with the corrected Up key. It retains complete media ZIP import, Japanese
font ROM import, custom PNG shells, raw disks up to 4 GiB, a 3D PCB explorer,
and bundled native emulation with guest audio and persistent writes to private
disk copies. Windows 95
is experimental: an intermittent guest VMM crash and a DOS text-layout issue
remain. See [release notes](desktop/RELEASE-MACOS-1.0.3.md) and
[validation limits](desktop/QA-MACOS-1.0.3.md). No proprietary media is included.

Older 1.0.0 portable downloads use the portable core without the full emulator or guest audio.
The [Pinokio launcher](https://github.com/ahmadexp/pc110-atlas-pinokio) is a separate
distribution channel; its pinned versions do not change with this Homebrew update.
Import your own compatible media; guest compatibility varies.

[Mac 1.0.3 downloads and checksums](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.3)
are separate from the [1.0.0 portable desktop downloads](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/desktop-v1.0.0).
The historical
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
The package downloads the public MSI and verifies its checksum. Version 1.0.0
was [approved by Chocolatey on September 23, 2026](https://community.chocolatey.org/packages/pc110-atlas/1.0.0).
Install directly from the Community Repository:

```powershell
choco install pc110-atlas
```

macOS 12 or later, Intel or Apple silicon:

```sh
brew tap ahmadexp/pc110-atlas
brew trust --cask ahmadexp/pc110-atlas/pc110-atlas
brew install --cask pc110-atlas
```

Homebrew 6 and later require trust for third-party packages. This trusts only
the PC110 Atlas cask, not the entire tap. Only grant trust if you trust this
project's package code to run with your user privileges. See
[Homebrew's tap trust documentation](https://docs.brew.sh/Tap-Trust).

For a one-command installation, including on older Homebrew versions without
the `trust` command, use the fully qualified name. Homebrew 6 and later grant
trust only to this cask:

```sh
brew install --cask ahmadexp/pc110-atlas/pc110-atlas
```

Alternatively, open the DMG matching your Mac and drag PC110 Atlas to Applications.
For an existing Homebrew installation, run `brew update` followed by
`brew upgrade --cask pc110-atlas`. Shut down the guest and back up your media first.
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
- [Mac 1.0.3 changes and known limits](desktop/RELEASE-MACOS-1.0.3.md)
- [Media ZIPs, font ROM and custom shells](desktop/MEDIA-PACKAGES.md)
- [IRIX build and testing](unix/README.md)
- [Publishing guide](desktop/DISTRIBUTION.md)
- [License scope and third-party terms](LICENSING.md)
- [Privacy](PRIVACY.md)
- [Report an issue](https://github.com/ahmadexp/homebrew-pc110-atlas/issues)

The original application code is MIT licensed. Hardware material retains
its existing terms. This is an independent project and is not affiliated
with or endorsed by IBM.
