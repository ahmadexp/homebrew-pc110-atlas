# PC110 Atlas downloads

Explore the IBM Palm Top PC 110 through an interactive hardware reference,
historical archive, and portable emulator. Import your own compatible BIOS
and raw disk images. IBM firmware and operating-system media are not included.

This repository hosts public releases, the Homebrew tap, package publishing
workflows, store assets, and the experimental IRIX source edition.

## Availability

The first desktop release is being prepared. Installation commands below
become usable after the corresponding channel has been published. Check
[Releases](https://github.com/ahmadexp/homebrew-pc110-atlas/releases) for the
available files and their release notes.

| Channel | Target | Initial status |
| --- | --- | --- |
| Snap Store | Ubuntu amd64 / arm64 | Publisher account registration pending |
| APT | Ubuntu/Debian amd64 / arm64 | Signed repository publication pending |
| YUM/DNF | Compatible x86_64 / aarch64 Linux | Signed repository publication pending |
| Chocolatey | Windows x64 | Publisher account configuration pending |
| Homebrew | macOS Intel / Apple silicon | Notarized release pending |
| IRIX | IRIX 6.5 MIPS n32 source | Experimental, hardware testing pending |

## Install

Ubuntu Snap Store, once available:

```sh
sudo snap install pc110-atlas
```

APT and YUM/DNF installation instructions and the signing-key fingerprint
will be published at [the package repository](https://ahmadexp.github.io/homebrew-pc110-atlas/).

Repository signing-key fingerprint:
`4B6FA5B0B9C8CC49F0C164C66D199F8D554224BC`.
The [public key](desktop/packaging/keys/pc110-atlas.asc) expires September 13, 2028.

Windows, once the Chocolatey submission is accepted:

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
