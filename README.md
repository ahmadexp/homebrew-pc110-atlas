# PC110 Atlas downloads

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator. Import your own compatible BIOS
and raw disk images. IBM firmware and operating-system media are not included.

This repository hosts public releases, the Homebrew tap, package publishing
workflows, store assets, and the experimental IRIX source edition.

## Availability

Linux and Windows installers, signed APT and YUM/DNF repositories, tested
Snap and Chocolatey packages, and the experimental IRIX source kit are available. Check
[Releases](https://github.com/ahmadexp/homebrew-pc110-atlas/releases) for the
available files and their release notes.

| Channel | Target | Status |
| --- | --- | --- |
| Snap Store | Ubuntu amd64 / arm64 | [Published to stable](https://snapcraft.io/pc110-atlas) |
| APT | Ubuntu/Debian amd64 / arm64 | [Signed repository live](https://ahmadexp.github.io/homebrew-pc110-atlas/) |
| YUM/DNF | Compatible x86_64 / aarch64 Linux | [Signed repository live](https://ahmadexp.github.io/homebrew-pc110-atlas/) |
| Chocolatey | Windows x64 | [Submitted](https://github.com/ahmadexp/homebrew-pc110-atlas/actions/runs/34869323670); automated review and moderator approval pending |
| Homebrew | macOS Intel / Apple silicon | Notarized release pending |
| IRIX | IRIX 6.5 MIPS n32 source | [Test kit available](https://github.com/ahmadexp/homebrew-pc110-atlas/releases/tag/irix-v1.0.0), hardware testing pending |

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

macOS, once the signed and notarized DMGs are available:

```sh
brew tap ahmadexp/pc110-atlas
brew install --cask pc110-atlas
```

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
